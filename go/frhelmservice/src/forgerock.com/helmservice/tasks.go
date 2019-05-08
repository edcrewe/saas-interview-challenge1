package main

import (
	"context"
	"fmt"
	"time"

	opentracing "github.com/opentracing/opentracing-go"
	opentracing_log "github.com/opentracing/opentracing-go/log"

	"github.com/RichardKnop/machinery/v1/log"
	"github.com/RichardKnop/machinery/v1/tasks"
	"github.com/google/uuid"

	tracers "github.com/RichardKnop/machinery/example/tracers"
)

func main() {
	send()
}

// Create two stub tasks and send them in parallel
func send() error {
	cleanup, err := tracers.SetupTracer("sender")
	if err != nil {
		log.FATAL.Fatalln("Unable to instantiate a tracer:", err)
	}
	defer cleanup()

	server, err := startServer()
	if err != nil {
		return err
	}

	var (
		addTask0, addTask1 tasks.Signature
	)

	var initTasks = func() {
		addTask0 = tasks.Signature{
			Name: "longadd",
			Args: []tasks.Arg{
				{
					Type:  "int64",
					Value: 1,
				},
				{
					Type:  "int64",
					Value: 1,
				},
			},
		}

		addTask1 = tasks.Signature{
			Name: "download",
			Args: []tasks.Arg{
			},
		}

	}
	/*
	 * Lets start a span representing this run of the `send` command and
	 * set a batch id as baggage so it can travel all the way into
	 * the worker functions.
	 */
	span, ctx := opentracing.StartSpanFromContext(context.Background(), "send")
	defer span.Finish()

	batchID := uuid.New().String()
	span.SetBaggageItem("batch.id", batchID)
	span.LogFields(opentracing_log.String("batch.id", batchID))

	log.INFO.Println("Starting batch:", batchID)

	// parallel execution of two tasks
	initTasks()
	log.INFO.Println("Group of tasks (parallel execution):")

	group, err := tasks.NewGroup(&addTask0, &addTask1)
	if err != nil {
		return fmt.Errorf("Error creating group: %s", err.Error())
	}

	asyncResults, err := server.SendGroupWithContext(ctx, group, 10)
	if err != nil {
		return fmt.Errorf("Could not send group: %s", err.Error())
	}

	for _, asyncResult := range asyncResults {
		results, err := asyncResult.Get(time.Duration(time.Millisecond * 5))
		if err != nil {
			log.WARNING.Printf(err.Error())
			return fmt.Errorf("Getting task result failed with error: %s", err.Error())
		}
		log.INFO.Printf(
			"result = %v\n",
			tasks.HumanReadableResults(results),
		)
	}

	return nil
}
