// Run the server for running a worker or sending tasks to
package main

import (
	"github.com/RichardKnop/machinery/v1"
	"github.com/RichardKnop/machinery/v1/config"

	helmtasks "forgerock.com/helmservice/helmtasks"
)

var taskmap  map[string]interface{}

func startServer() (*machinery.Server, error) {
	cnf, err := config.NewFromYaml("config.yml", true)
	if err != nil {
		return nil, err
	}

	// Create server instance
	server, err := machinery.NewServer(cnf)
	if err != nil {
		return nil, err
	}

	// Register tasks
	taskmap = map[string]interface{}{
		"longadd":           helmtasks.LongtimeAdd,
		"download":          helmtasks.ChartDownload,
	}

	return server, server.RegisterTasks(taskmap)
}
