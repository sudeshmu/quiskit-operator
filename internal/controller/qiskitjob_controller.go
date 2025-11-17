/*
Copyright 2025 Quantum Operator Team.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controller

import (
	"context"
	"fmt"
	"time"

	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/api/resource"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	"sigs.k8s.io/controller-runtime/pkg/log"

	quantumv1 "github.com/quantum-operator/qiskit-operator/api/v1"
)

// Job phase constants
const (
	PhasePending    = "Pending"
	PhaseValidating = "Validating"
	PhaseScheduling = "Scheduling"
	PhaseRunning    = "Running"
	PhaseCompleted  = "Completed"
	PhaseFailed     = "Failed"
	PhaseCancelled  = "Cancelled"
	PhaseRetrying   = "Retrying"
)

// Finalizer name
const qiskitJobFinalizer = "quantum.io/finalizer"

// QiskitJobReconciler reconciles a QiskitJob object
type QiskitJobReconciler struct {
	client.Client
	Scheme               *runtime.Scheme
	ValidationServiceURL string
}

// +kubebuilder:rbac:groups=quantum.quantum.io,resources=qiskitjobs,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=quantum.quantum.io,resources=qiskitjobs/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=quantum.quantum.io,resources=qiskitjobs/finalizers,verbs=update
// +kubebuilder:rbac:groups="",resources=pods,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups="",resources=pods/log,verbs=get;list
// +kubebuilder:rbac:groups="",resources=configmaps,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups="",resources=secrets,verbs=get;list;watch
// +kubebuilder:rbac:groups="",resources=events,verbs=create;patch

// Reconcile is part of the main kubernetes reconciliation loop which aims to
// move the current state of the cluster closer to the desired state.
//
// The reconciler implements a phase-based state machine:
// Pending → Validating → Scheduling → Running → Completed/Failed
func (r *QiskitJobReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)

	// Fetch the QiskitJob instance
	var job quantumv1.QiskitJob
	if err := r.Get(ctx, req.NamespacedName, &job); err != nil {
		if errors.IsNotFound(err) {
			// Object not found, could have been deleted
			logger.Info("QiskitJob not found, likely deleted")
			return ctrl.Result{}, nil
		}
		// Error reading the object - requeue the request
		logger.Error(err, "Failed to get QiskitJob")
		return ctrl.Result{}, err
	}

	// Handle deletion with finalizer
	if job.ObjectMeta.DeletionTimestamp != nil {
		if controllerutil.ContainsFinalizer(&job, qiskitJobFinalizer) {
			// Run cleanup logic
			if err := r.cleanupJob(ctx, &job); err != nil {
				logger.Error(err, "Failed to cleanup job")
				return ctrl.Result{}, err
			}

			// Remove finalizer
			controllerutil.RemoveFinalizer(&job, qiskitJobFinalizer)
			if err := r.Update(ctx, &job); err != nil {
				return ctrl.Result{}, err
			}
		}
		return ctrl.Result{}, nil
	}

	// Add finalizer if it doesn't exist
	if !controllerutil.ContainsFinalizer(&job, qiskitJobFinalizer) {
		controllerutil.AddFinalizer(&job, qiskitJobFinalizer)
		if err := r.Update(ctx, &job); err != nil {
			return ctrl.Result{}, err
		}
	}

	// Initialize phase if empty
	if job.Status.Phase == "" {
		job.Status.Phase = PhasePending
		job.Status.Message = "Job created, awaiting validation"
		now := metav1.Now()
		job.Status.StartTime = &now
		if err := r.Status().Update(ctx, &job); err != nil {
			logger.Error(err, "Failed to update job status")
			return ctrl.Result{}, err
		}
		logger.Info("Job initialized", "phase", PhasePending)
		return ctrl.Result{Requeue: true}, nil
	}

	// Phase-based reconciliation
	logger.Info("Reconciling QiskitJob", 
		"name", job.Name, 
		"namespace", job.Namespace, 
		"phase", job.Status.Phase)

	var result ctrl.Result
	var err error

	switch job.Status.Phase {
	case PhasePending:
		result, err = r.handlePendingJob(ctx, &job)
	case PhaseValidating:
		result, err = r.handleValidatingJob(ctx, &job)
	case PhaseScheduling:
		result, err = r.handleSchedulingJob(ctx, &job)
	case PhaseRunning:
		result, err = r.handleRunningJob(ctx, &job)
	case PhaseCompleted:
		result, err = r.handleCompletedJob(ctx, &job)
	case PhaseFailed:
		result, err = r.handleFailedJob(ctx, &job)
	case PhaseRetrying:
		result, err = r.handleRetryingJob(ctx, &job)
	default:
		logger.Info("Unknown phase, resetting to Pending", "phase", job.Status.Phase)
		job.Status.Phase = PhasePending
		err = r.Status().Update(ctx, &job)
		result = ctrl.Result{Requeue: true}
	}

	if err != nil {
		logger.Error(err, "Error handling job phase", "phase", job.Status.Phase)
		// Don't return error for retryable issues, just requeue
		return ctrl.Result{RequeueAfter: 10 * time.Second}, nil
	}

	return result, nil
}

// Phase handlers

// handlePendingJob validates the job specification
func (r *QiskitJobReconciler) handlePendingJob(ctx context.Context, job *quantumv1.QiskitJob) (ctrl.Result, error) {
	logger := log.FromContext(ctx)
	logger.Info("Handling pending job")

	// Basic validation
	if job.Spec.Backend.Type == "" {
		return r.updateJobPhase(ctx, job, PhaseFailed, "Backend type is required")
	}

	if job.Spec.Circuit.Source == "" {
		return r.updateJobPhase(ctx, job, PhaseFailed, "Circuit source is required")
	}

	if job.Spec.Circuit.Source == "inline" && job.Spec.Circuit.Code == "" {
		return r.updateJobPhase(ctx, job, PhaseFailed, "Circuit code is required for inline source")
	}

	// Move to validation phase
	return r.updateJobPhase(ctx, job, PhaseValidating, "Job specification validated, starting circuit validation")
}

// handleValidatingJob validates the quantum circuit
func (r *QiskitJobReconciler) handleValidatingJob(ctx context.Context, job *quantumv1.QiskitJob) (ctrl.Result, error) {
	logger := log.FromContext(ctx)
	logger.Info("Validating quantum circuit")

	// TODO: Call validation service
	// For now, we'll skip validation service and move to scheduling
	// In production, this would call the Python validation service

	// Mock circuit metadata for now
	if job.Status.CircuitMetadata == nil {
		job.Status.CircuitMetadata = &quantumv1.CircuitMetadata{
			Hash:   "mock-hash",
			Depth:  10,
			Qubits: 2,
			Gates:  15,
			GateTypes: map[string]int{
				"h":       2,
				"cx":      5,
				"measure": 2,
			},
		}
	}

	return r.updateJobPhase(ctx, job, PhaseScheduling, "Circuit validated successfully")
}

// handleSchedulingJob selects the backend and prepares for execution
func (r *QiskitJobReconciler) handleSchedulingJob(ctx context.Context, job *quantumv1.QiskitJob) (ctrl.Result, error) {
	logger := log.FromContext(ctx)
	logger.Info("Scheduling job for execution")

	// For MVP, we only support local_simulator
	if job.Spec.Backend.Type != "local_simulator" {
		return r.updateJobPhase(ctx, job, PhaseFailed, 
			fmt.Sprintf("Backend type '%s' not yet supported, use 'local_simulator'", job.Spec.Backend.Type))
	}

	// Set selected backend
	job.Status.SelectedBackend = "local_simulator"
	job.Status.EstimatedCost = "$0.00" // Local simulator is free

	// Update status
	if err := r.Status().Update(ctx, job); err != nil {
		return ctrl.Result{}, err
	}

	// Move to running phase
	return r.updateJobPhase(ctx, job, PhaseRunning, "Backend selected, creating execution pod")
}

// handleRunningJob manages the execution pod
func (r *QiskitJobReconciler) handleRunningJob(ctx context.Context, job *quantumv1.QiskitJob) (ctrl.Result, error) {
	logger := log.FromContext(ctx)
	logger.Info("Handling running job")

	// Check if execution pod exists
	podName := fmt.Sprintf("qiskit-job-%s", job.Name)
	var pod corev1.Pod
	err := r.Get(ctx, types.NamespacedName{Name: podName, Namespace: job.Namespace}, &pod)

	if err != nil && errors.IsNotFound(err) {
		// Pod doesn't exist, create it
		logger.Info("Creating execution pod")
		pod, err := r.createExecutionPod(ctx, job)
		if err != nil {
			logger.Error(err, "Failed to create execution pod")
			return r.updateJobPhase(ctx, job, PhaseFailed, fmt.Sprintf("Failed to create pod: %v", err))
		}

		if err := r.Create(ctx, pod); err != nil {
			logger.Error(err, "Failed to create pod in cluster")
			return ctrl.Result{}, err
		}

		logger.Info("Execution pod created", "pod", podName)
		job.Status.JobID = podName
		if err := r.Status().Update(ctx, job); err != nil {
			return ctrl.Result{}, err
		}

		// Requeue to check pod status
		return ctrl.Result{RequeueAfter: 5 * time.Second}, nil
	} else if err != nil {
		logger.Error(err, "Failed to get pod")
		return ctrl.Result{}, err
	}

	// Pod exists, check its status
	logger.Info("Checking pod status", "phase", pod.Status.Phase)

	switch pod.Status.Phase {
	case corev1.PodPending:
		job.Status.Message = "Execution pod is pending"
		r.Status().Update(ctx, job)
		return ctrl.Result{RequeueAfter: 5 * time.Second}, nil

	case corev1.PodRunning:
		job.Status.Message = "Quantum circuit is executing"
		r.Status().Update(ctx, job)
		return ctrl.Result{RequeueAfter: 5 * time.Second}, nil

	case corev1.PodSucceeded:
		logger.Info("Pod completed successfully")
		return r.handlePodCompletion(ctx, job, &pod)

	case corev1.PodFailed:
		logger.Info("Pod failed")
		return r.updateJobPhase(ctx, job, PhaseFailed, "Execution pod failed")

	default:
		job.Status.Message = fmt.Sprintf("Unknown pod phase: %s", pod.Status.Phase)
		r.Status().Update(ctx, job)
		return ctrl.Result{RequeueAfter: 5 * time.Second}, nil
	}
}

// handlePodCompletion processes completed pod and stores results
func (r *QiskitJobReconciler) handlePodCompletion(ctx context.Context, job *quantumv1.QiskitJob, pod *corev1.Pod) (ctrl.Result, error) {
	logger := log.FromContext(ctx)
	logger.Info("Processing pod completion")

	// Get pod logs (results)
	// In production, we'd parse actual results from logs or mounted volume
	// For MVP, we'll just mark as complete

	// Update job status
	now := metav1.Now()
	job.Status.CompletionTime = &now
	job.Status.ActualCost = "$0.00"

	// Calculate execution time
	if job.Status.StartTime != nil {
		duration := now.Sub(job.Status.StartTime.Time)
		job.Status.Metrics = &quantumv1.ExecutionMetrics{
			TotalTime:     duration.String(),
			ExecutionTime: duration.String(),
		}
	}

	// Create results ConfigMap if specified
	if job.Spec.Output != nil && job.Spec.Output.Type == "configmap" {
		if err := r.createResultsConfigMap(ctx, job); err != nil {
			logger.Error(err, "Failed to create results ConfigMap")
		}
	}

	return r.updateJobPhase(ctx, job, PhaseCompleted, "Job completed successfully")
}

// handleCompletedJob manages completed jobs
func (r *QiskitJobReconciler) handleCompletedJob(ctx context.Context, job *quantumv1.QiskitJob) (ctrl.Result, error) {
	// Job is complete, no further action needed
	// Could implement cleanup logic here
	return ctrl.Result{}, nil
}

// handleFailedJob manages failed jobs
func (r *QiskitJobReconciler) handleFailedJob(ctx context.Context, job *quantumv1.QiskitJob) (ctrl.Result, error) {
	logger := log.FromContext(ctx)
	
	// Check if we should retry
	maxRetries := 3
	if job.Status.RetryCount < maxRetries {
		logger.Info("Job failed, attempting retry", "retryCount", job.Status.RetryCount)
		job.Status.RetryCount++
		job.Status.Phase = PhaseRetrying
		now := metav1.Now()
		retryTime := now.Add(10 * time.Second)
		job.Status.NextRetryAt = &metav1.Time{Time: retryTime}
		return ctrl.Result{RequeueAfter: 10 * time.Second}, r.Status().Update(ctx, job)
	}

	// Max retries exceeded, job stays failed
	logger.Info("Max retries exceeded, job permanently failed")
	return ctrl.Result{}, nil
}

// handleRetryingJob manages job retries
func (r *QiskitJobReconciler) handleRetryingJob(ctx context.Context, job *quantumv1.QiskitJob) (ctrl.Result, error) {
	logger := log.FromContext(ctx)
	logger.Info("Retrying job", "retryCount", job.Status.RetryCount)

	// Reset to pending to restart the flow
	return r.updateJobPhase(ctx, job, PhasePending, fmt.Sprintf("Retrying job (attempt %d)", job.Status.RetryCount))
}

// Helper functions

// updateJobPhase updates the job phase and message
func (r *QiskitJobReconciler) updateJobPhase(ctx context.Context, job *quantumv1.QiskitJob, phase, message string) (ctrl.Result, error) {
	logger := log.FromContext(ctx)
	
	oldPhase := job.Status.Phase
	job.Status.Phase = phase
	job.Status.Message = message

	if err := r.Status().Update(ctx, job); err != nil {
		logger.Error(err, "Failed to update job status")
		return ctrl.Result{}, err
	}

	logger.Info("Job phase updated", "from", oldPhase, "to", phase, "message", message)

	// Requeue immediately to process next phase
	return ctrl.Result{Requeue: true}, nil
}

// cleanupJob performs cleanup when job is deleted
func (r *QiskitJobReconciler) cleanupJob(ctx context.Context, job *quantumv1.QiskitJob) error {
	logger := log.FromContext(ctx)
	logger.Info("Cleaning up job resources")

	// Delete execution pod if it exists
	podName := fmt.Sprintf("qiskit-job-%s", job.Name)
	pod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      podName,
			Namespace: job.Namespace,
		},
	}

	if err := r.Delete(ctx, pod); err != nil && !errors.IsNotFound(err) {
		return err
	}

	logger.Info("Job cleanup complete")
	return nil
}

// createExecutionPod creates a pod to execute the quantum circuit
func (r *QiskitJobReconciler) createExecutionPod(ctx context.Context, job *quantumv1.QiskitJob) (*corev1.Pod, error) {
	podName := fmt.Sprintf("qiskit-job-%s", job.Name)

	// Get execution parameters
	shots := 1024
	if job.Spec.Execution.Shots > 0 {
		shots = job.Spec.Execution.Shots
	}

	pod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{
			Name:      podName,
			Namespace: job.Namespace,
			Labels: map[string]string{
				"app":                       "qiskit-operator",
				"qiskit-job":                job.Name,
				"quantum.io/job":            job.Name,
				"quantum.io/backend-type":   job.Spec.Backend.Type,
			},
		},
		Spec: corev1.PodSpec{
			RestartPolicy: corev1.RestartPolicyNever,
			Containers: []corev1.Container{
				{
					Name:  "executor",
					Image: "python:3.11-slim", // TODO: Use custom image with Qiskit
					Command: []string{
						"sh", "-c",
						fmt.Sprintf(`
pip install --quiet qiskit==1.0.0 qiskit-aer==0.13.0 && \
python3 -c "%s"
`, r.escapeCode(job.Spec.Circuit.Code)),
					},
					Env: []corev1.EnvVar{
						{
							Name:  "SHOTS",
							Value: fmt.Sprintf("%d", shots),
						},
						{
							Name:  "OPTIMIZATION_LEVEL",
							Value: fmt.Sprintf("%d", job.Spec.Execution.OptimizationLevel),
						},
					},
					Resources: corev1.ResourceRequirements{
						Requests: corev1.ResourceList{
							corev1.ResourceCPU:    mustParseQuantity("500m"),
							corev1.ResourceMemory: mustParseQuantity("1Gi"),
						},
						Limits: corev1.ResourceList{
							corev1.ResourceCPU:    mustParseQuantity("2"),
							corev1.ResourceMemory: mustParseQuantity("4Gi"),
						},
					},
					SecurityContext: &corev1.SecurityContext{
						RunAsNonRoot:             ptr(true),
						RunAsUser:                ptr(int64(1000)),
						AllowPrivilegeEscalation: ptr(false),
						Capabilities: &corev1.Capabilities{
							Drop: []corev1.Capability{"ALL"},
						},
					},
				},
			},
		},
	}

	// Set owner reference
	if err := controllerutil.SetControllerReference(job, pod, r.Scheme); err != nil {
		return nil, err
	}

	return pod, nil
}

// createResultsConfigMap creates a ConfigMap with job results
func (r *QiskitJobReconciler) createResultsConfigMap(ctx context.Context, job *quantumv1.QiskitJob) error {
	logger := log.FromContext(ctx)

	if job.Spec.Output == nil || job.Spec.Output.Location == "" {
		return nil
	}

	// Create results data (mock for now)
	resultsData := fmt.Sprintf(`{
  "job_id": "%s",
  "job_name": "%s",
  "backend": "%s",
  "shots": %d,
  "results": {
    "counts": {
      "00": 512,
      "11": 512
    }
  },
  "status": "completed"
}`, job.Status.JobID, job.Name, job.Status.SelectedBackend, job.Spec.Execution.Shots)

	cm := &corev1.ConfigMap{
		ObjectMeta: metav1.ObjectMeta{
			Name:      job.Spec.Output.Location,
			Namespace: job.Namespace,
			Labels: map[string]string{
				"app":            "qiskit-operator",
				"quantum.io/job": job.Name,
			},
		},
		Data: map[string]string{
			"results.json": resultsData,
		},
	}

	// Set owner reference
	if err := controllerutil.SetControllerReference(job, cm, r.Scheme); err != nil {
		return err
	}

	// Create or update ConfigMap
	existing := &corev1.ConfigMap{}
	err := r.Get(ctx, types.NamespacedName{Name: cm.Name, Namespace: cm.Namespace}, existing)
	if err != nil && errors.IsNotFound(err) {
		logger.Info("Creating results ConfigMap", "name", cm.Name)
		return r.Create(ctx, cm)
	} else if err != nil {
		return err
	}

	// Update existing ConfigMap
	existing.Data = cm.Data
	logger.Info("Updating results ConfigMap", "name", cm.Name)
	return r.Update(ctx, existing)
}

// escapeCode escapes the circuit code for shell execution
func (r *QiskitJobReconciler) escapeCode(code string) string {
	// Basic escaping - in production, use proper shell escaping
	// For now, just handle quotes
	code = fmt.Sprintf("%s", code)
	return code
}

// Helper functions for pointer values
func ptr[T any](v T) *T {
	return &v
}

func mustParseQuantity(s string) resource.Quantity {
	q, err := resource.ParseQuantity(s)
	if err != nil {
		panic(fmt.Sprintf("invalid quantity: %s", s))
	}
	return q
}

// SetupWithManager sets up the controller with the Manager.
func (r *QiskitJobReconciler) SetupWithManager(mgr ctrl.Manager) error {
	// Set default validation service URL
	if r.ValidationServiceURL == "" {
		r.ValidationServiceURL = "http://validation-service:8000"
	}

	return ctrl.NewControllerManagedBy(mgr).
		For(&quantumv1.QiskitJob{}).
		Owns(&corev1.Pod{}).
		Named("qiskitjob").
		Complete(r)
}
