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

package v1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EDIT THIS FILE!  THIS IS SCAFFOLDING FOR YOU TO OWN!
// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// QiskitJobSpec defines the desired state of QiskitJob
type QiskitJobSpec struct {
	// Backend configuration for quantum execution
	// +required
	Backend BackendSpec `json:"backend"`

	// Circuit definition (Qiskit Python code)
	// +required
	Circuit CircuitSpec `json:"circuit"`

	// Execution parameters (shots, optimization level, etc.)
	// +optional
	Execution ExecutionSpec `json:"execution,omitempty"`

	// Session configuration for IBM Quantum Runtime sessions
	// +optional
	Session *SessionSpec `json:"session,omitempty"`

	// Resource requirements for execution pods
	// +optional
	Resources *ResourceRequirements `json:"resources,omitempty"`

	// Budget constraints and cost management
	// +optional
	Budget *BudgetSpec `json:"budget,omitempty"`

	// Output configuration (where to store results)
	// +optional
	Output *OutputSpec `json:"output,omitempty"`

	// Credentials for backend authentication
	// +optional
	Credentials *CredentialsSpec `json:"credentials,omitempty"`

	// Backend selection preferences
	// +optional
	BackendSelection *BackendSelectionSpec `json:"backendSelection,omitempty"`
}

// BackendSpec defines the quantum backend configuration
type BackendSpec struct {
	// Type of backend (ibm_quantum, ibm_simulator, aws_braket, local_simulator)
	// +kubebuilder:validation:Enum=ibm_quantum;ibm_simulator;aws_braket;local_simulator
	// +required
	Type string `json:"type"`

	// Name of the specific backend (e.g., "ibm_brisbane")
	// +optional
	Name string `json:"name,omitempty"`

	// IBM Cloud instance CRN for enterprise accounts
	// +optional
	Instance string `json:"instance,omitempty"`

	// IBM Quantum Network hub (legacy authentication)
	// +optional
	Hub string `json:"hub,omitempty"`

	// IBM Quantum Network group (legacy authentication)
	// +optional
	Group string `json:"group,omitempty"`

	// IBM Quantum Network project (legacy authentication)
	// +optional
	Project string `json:"project,omitempty"`
}

// CircuitSpec defines the quantum circuit configuration
type CircuitSpec struct {
	// Source of the circuit code (inline, configmap, url, git)
	// +kubebuilder:validation:Enum=inline;configmap;url;git
	// +required
	Source string `json:"source"`

	// Inline Qiskit Python code
	// +optional
	Code string `json:"code,omitempty"`

	// ConfigMap reference for circuit code
	// +optional
	ConfigMapRef *ConfigMapRef `json:"configMapRef,omitempty"`

	// URL to fetch circuit code
	// +optional
	URL string `json:"url,omitempty"`

	// Git repository reference
	// +optional
	GitRef *GitRef `json:"gitRef,omitempty"`
}

// ConfigMapRef references a ConfigMap
type ConfigMapRef struct {
	// Name of the ConfigMap
	// +required
	Name string `json:"name"`

	// Key in the ConfigMap
	// +required
	Key string `json:"key"`
}

// GitRef references a Git repository
type GitRef struct {
	// Repository URL
	// +required
	Repository string `json:"repository"`

	// Branch name
	// +optional
	Branch string `json:"branch,omitempty"`

	// Path to circuit file in repository
	// +required
	Path string `json:"path"`
}

// ExecutionSpec defines execution parameters
type ExecutionSpec struct {
	// Number of measurements (shots)
	// +kubebuilder:validation:Minimum=1
	// +kubebuilder:validation:Maximum=100000
	// +optional
	// +kubebuilder:default=1024
	Shots int `json:"shots,omitempty"`

	// Qiskit optimization level (0-3)
	// +kubebuilder:validation:Minimum=0
	// +kubebuilder:validation:Maximum=3
	// +optional
	// +kubebuilder:default=1
	OptimizationLevel int `json:"optimizationLevel,omitempty"`

	// IBM Quantum resilience level (0-2)
	// +kubebuilder:validation:Minimum=0
	// +kubebuilder:validation:Maximum=2
	// +optional
	ResilienceLevel int `json:"resilienceLevel,omitempty"`

	// Maximum execution time
	// +optional
	MaxExecutionTime string `json:"maxExecutionTime,omitempty"`

	// Job priority (low, normal, high, urgent)
	// +kubebuilder:validation:Enum=low;normal;high;urgent
	// +optional
	// +kubebuilder:default=normal
	Priority string `json:"priority,omitempty"`

	// Disable automatic fallback to simulator
	// +optional
	DisableFallback bool `json:"disableFallback,omitempty"`
}

// SessionSpec defines IBM Quantum Runtime session configuration
type SessionSpec struct {
	// Session name
	// +optional
	Name string `json:"name,omitempty"`

	// Maximum session time in seconds
	// +optional
	MaxTime int `json:"maxTime,omitempty"`

	// Session mode (dedicated, batch)
	// +kubebuilder:validation:Enum=dedicated;batch
	// +optional
	Mode string `json:"mode,omitempty"`
}

// ResourceRequirements defines pod resource requirements
type ResourceRequirements struct {
	// Resource requests
	// +optional
	Requests map[string]string `json:"requests,omitempty"`

	// Resource limits
	// +optional
	Limits map[string]string `json:"limits,omitempty"`
}

// BudgetSpec defines cost constraints
type BudgetSpec struct {
	// Maximum cost for this job (e.g., "$10.00")
	// +optional
	MaxCost string `json:"maxCost,omitempty"`

	// Cost center identifier
	// +optional
	CostCenter string `json:"costCenter,omitempty"`

	// Billing account
	// +optional
	BillingAccount string `json:"billingAccount,omitempty"`
}

// OutputSpec defines where to store results
type OutputSpec struct {
	// Output type (pvc, s3, gcs, azure_blob, configmap)
	// +kubebuilder:validation:Enum=pvc;s3;gcs;azure_blob;configmap
	// +required
	Type string `json:"type"`

	// Storage location (PVC name, bucket name, etc.)
	// +required
	Location string `json:"location"`

	// Path within the storage location
	// +optional
	Path string `json:"path,omitempty"`

	// Result format (json, pickle, qpy, csv)
	// +kubebuilder:validation:Enum=json;pickle;qpy;csv
	// +optional
	// +kubebuilder:default=json
	Format string `json:"format,omitempty"`

	// Retention period
	// +optional
	Retention string `json:"retention,omitempty"`
}

// CredentialsSpec defines authentication credentials
type CredentialsSpec struct {
	// Kubernetes Secret reference
	// +optional
	SecretRef *SecretRef `json:"secretRef,omitempty"`

	// HashiCorp Vault path
	// +optional
	VaultPath string `json:"vaultPath,omitempty"`
}

// SecretRef references a Kubernetes Secret
type SecretRef struct {
	// Secret name
	// +required
	Name string `json:"name"`

	// Secret namespace
	// +optional
	Namespace string `json:"namespace,omitempty"`
}

// BackendSelectionSpec defines backend selection preferences
type BackendSelectionSpec struct {
	// Selection weights for scoring backends
	// +optional
	Weights *BackendWeights `json:"weights,omitempty"`

	// Preferred backends (ordered by preference)
	// +optional
	PreferredBackends []string `json:"preferredBackends,omitempty"`

	// Excluded backends
	// +optional
	ExcludedBackends []string `json:"excludedBackends,omitempty"`

	// Allow fallback to simulator
	// +optional
	AllowFallback bool `json:"allowFallback,omitempty"`

	// Fallback to simulator on errors
	// +optional
	FallbackToSimulator bool `json:"fallbackToSimulator,omitempty"`
}

// BackendWeights defines scoring weights for backend selection
type BackendWeights struct {
	// Cost weight (0.0-1.0)
	// +optional
	Cost float64 `json:"cost,omitempty"`

	// Queue time weight (0.0-1.0)
	// +optional
	QueueTime float64 `json:"queueTime,omitempty"`

	// Capability weight (0.0-1.0)
	// +optional
	Capability float64 `json:"capability,omitempty"`

	// Availability weight (0.0-1.0)
	// +optional
	Availability float64 `json:"availability,omitempty"`
}

// QiskitJobStatus defines the observed state of QiskitJob.
type QiskitJobStatus struct {
	// Phase of the job lifecycle
	// +optional
	Phase string `json:"phase,omitempty"`

	// Human-readable message about the current state
	// +optional
	Message string `json:"message,omitempty"`

	// Job start time
	// +optional
	StartTime *metav1.Time `json:"startTime,omitempty"`

	// Job completion time
	// +optional
	CompletionTime *metav1.Time `json:"completionTime,omitempty"`

	// Selected backend for execution
	// +optional
	SelectedBackend string `json:"selectedBackend,omitempty"`

	// Original backend if fallback was used
	// +optional
	OriginalBackend string `json:"originalBackend,omitempty"`

	// Whether fallback to simulator was used
	// +optional
	FallbackUsed bool `json:"fallbackUsed,omitempty"`

	// Backend information
	// +optional
	BackendInfo *BackendInfo `json:"backendInfo,omitempty"`

	// Estimated cost for this job
	// +optional
	EstimatedCost string `json:"estimatedCost,omitempty"`

	// Actual cost after execution
	// +optional
	ActualCost string `json:"actualCost,omitempty"`

	// Current position in backend queue
	// +optional
	QueuePosition *int `json:"queuePosition,omitempty"`

	// Estimated start time based on queue
	// +optional
	EstimatedStartTime *metav1.Time `json:"estimatedStartTime,omitempty"`

	// IBM Quantum job ID
	// +optional
	JobID string `json:"jobId,omitempty"`

	// Results information
	// +optional
	Results *ResultsInfo `json:"results,omitempty"`

	// Execution metrics
	// +optional
	Metrics *ExecutionMetrics `json:"metrics,omitempty"`

	// Retry information
	// +optional
	RetryCount int `json:"retryCount,omitempty"`

	// Next retry time
	// +optional
	NextRetryAt *metav1.Time `json:"nextRetryAt,omitempty"`

	// Circuit metadata (from validation)
	// +optional
	CircuitMetadata *CircuitMetadata `json:"circuitMetadata,omitempty"`

	// Conditions represent the current state of the QiskitJob resource
	// +listType=map
	// +listMapKey=type
	// +optional
	Conditions []metav1.Condition `json:"conditions,omitempty"`
}

// BackendInfo contains information about the selected backend
type BackendInfo struct {
	// Backend name
	// +optional
	Name string `json:"name,omitempty"`

	// Backend version
	// +optional
	Version string `json:"version,omitempty"`

	// Number of qubits
	// +optional
	Qubits int `json:"qubits,omitempty"`

	// Average gate error rate
	// +optional
	GateError float64 `json:"gateError,omitempty"`

	// Average readout error rate
	// +optional
	ReadoutError float64 `json:"readoutError,omitempty"`
}

// ResultsInfo contains information about job results
type ResultsInfo struct {
	// Location of the results
	// +optional
	Location string `json:"location,omitempty"`

	// Number of shots executed
	// +optional
	Shots int `json:"shots,omitempty"`

	// Total execution time
	// +optional
	ExecutionTime string `json:"executionTime,omitempty"`

	// Quantum execution time (IBM specific)
	// +optional
	QuantumTime string `json:"quantumTime,omitempty"`

	// Success rate (0.0-1.0)
	// +optional
	SuccessRate float64 `json:"successRate,omitempty"`
}

// ExecutionMetrics contains detailed execution metrics
type ExecutionMetrics struct {
	// Time from submission to start
	// +optional
	SubmissionTime string `json:"submissionTime,omitempty"`

	// Time spent in queue
	// +optional
	QueueTime string `json:"queueTime,omitempty"`

	// Time spent executing
	// +optional
	ExecutionTime string `json:"executionTime,omitempty"`

	// Total time from submission to completion
	// +optional
	TotalTime string `json:"totalTime,omitempty"`

	// Memory usage
	// +optional
	MemoryUsage string `json:"memoryUsage,omitempty"`

	// CPU usage
	// +optional
	CPUUsage string `json:"cpuUsage,omitempty"`
}

// CircuitMetadata contains metadata about the circuit
type CircuitMetadata struct {
	// Circuit hash for caching
	// +optional
	Hash string `json:"hash,omitempty"`

	// Circuit depth
	// +optional
	Depth int `json:"depth,omitempty"`

	// Number of qubits
	// +optional
	Qubits int `json:"qubits,omitempty"`

	// Total number of gates
	// +optional
	Gates int `json:"gates,omitempty"`

	// Gate types and counts
	// +optional
	GateTypes map[string]int `json:"gateTypes,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:resource:shortName=qjob;qj
// +kubebuilder:printcolumn:name="Phase",type=string,JSONPath=`.status.phase`
// +kubebuilder:printcolumn:name="Backend",type=string,JSONPath=`.status.selectedBackend`
// +kubebuilder:printcolumn:name="Cost",type=string,JSONPath=`.status.actualCost`
// +kubebuilder:printcolumn:name="Age",type=date,JSONPath=`.metadata.creationTimestamp`

// QiskitJob is the Schema for the qiskitjobs API
type QiskitJob struct {
	metav1.TypeMeta `json:",inline"`

	// metadata is a standard object metadata
	// +optional
	metav1.ObjectMeta `json:"metadata,omitempty,omitzero"`

	// spec defines the desired state of QiskitJob
	// +required
	Spec QiskitJobSpec `json:"spec"`

	// status defines the observed state of QiskitJob
	// +optional
	Status QiskitJobStatus `json:"status,omitempty,omitzero"`
}

// +kubebuilder:object:root=true

// QiskitJobList contains a list of QiskitJob
type QiskitJobList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []QiskitJob `json:"items"`
}

func init() {
	SchemeBuilder.Register(&QiskitJob{}, &QiskitJobList{})
}
