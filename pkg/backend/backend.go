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

package backend

import (
	"context"
	"time"
)

// BackendType represents the type of quantum backend
type BackendType string

const (
	IBMQuantum      BackendType = "ibm_quantum"
	IBMSimulator    BackendType = "ibm_simulator"
	AWSBraket       BackendType = "aws_braket"
	LocalSimulator  BackendType = "local_simulator"
)

// Backend is the main interface for all quantum computing backends
type Backend interface {
	// Identification
	Name() string
	Type() BackendType
	Provider() string

	// Capabilities
	GetCapabilities(ctx context.Context) (*BackendCapabilities, error)
	IsAvailable(ctx context.Context) (bool, error)
	GetQueueStatus(ctx context.Context) (*QueueStatus, error)

	// Job Management
	SubmitJob(ctx context.Context, job *QuantumJob) (*JobID, error)
	GetJobStatus(ctx context.Context, jobID JobID) (*JobStatus, error)
	GetJobResult(ctx context.Context, jobID JobID) (*JobResult, error)
	CancelJob(ctx context.Context, jobID JobID) error

	// Cost Management
	EstimateCost(ctx context.Context, job *QuantumJob) (*CostEstimate, error)
	GetActualCost(ctx context.Context, jobID JobID) (*Cost, error)

	// Authentication
	Authenticate(ctx context.Context, credentials *Credentials) error
	RefreshCredentials(ctx context.Context) error
}

// BackendCapabilities describes what a backend can do
type BackendCapabilities struct {
	MaxQubits            int
	MaxShots             int
	SupportsDynamicCircuits bool
	SupportsPulse        bool
	GateSet              []string
	Connectivity         [][]int
	GateErrors           map[string]float64
	ReadoutErrors        []float64
}

// QueueStatus represents the current state of the backend queue
type QueueStatus struct {
	QueueLength          int
	EstimatedWaitSeconds int
	Position             *int // nil if not in queue
	EstimatedStartTime   *time.Time
}

// QuantumJob represents a quantum job to be executed
type QuantumJob struct {
	ID                string
	CircuitCode       string
	Shots             int
	OptimizationLevel int
	ResilienceLevel   int
	MaxExecutionTime  time.Duration
	Metadata          map[string]string
}

// JobID is a unique identifier for a submitted job
type JobID string

// JobStatus represents the current status of a job
type JobStatus struct {
	ID              JobID
	Phase           string // Pending, Queued, Running, Completed, Failed, Cancelled
	Message         string
	QueuePosition   *int
	EstimatedStart  *time.Time
	StartTime       *time.Time
	CompletionTime  *time.Time
	QuantumTime     *time.Duration
}

// JobResult contains the results of a completed quantum job
type JobResult struct {
	JobID           JobID
	Success         bool
	Counts          map[string]int
	Probabilities   map[string]float64
	Statevector     []complex128
	Metadata        map[string]interface{}
	ExecutionTime   time.Duration
	QuantumTime     time.Duration
	CircuitDepth    int
	CircuitQubits   int
	RawData         []byte // Raw backend-specific data
}

// CostEstimate provides an estimate of job cost
type CostEstimate struct {
	Amount       float64
	Currency     string
	QuantumTime  time.Duration
	ComputeTime  time.Duration
	Confidence   float64 // 0.0-1.0, how confident we are in this estimate
}

// Cost represents the actual cost of a completed job
type Cost struct {
	Amount      float64
	Currency    string
	QuantumTime time.Duration
	Breakdown   map[string]float64 // Detailed cost breakdown
}

// Credentials contains authentication information for a backend
type Credentials struct {
	APIKey   string
	Instance string // CRN for IBM Cloud
	Hub      string // IBM Quantum Network hub
	Group    string // IBM Quantum Network group
	Project  string // IBM Quantum Network project
	Region   string // AWS region, etc.
	Extra    map[string]string
}

