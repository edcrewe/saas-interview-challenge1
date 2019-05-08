package helmtasks

import (
	"time"
	"os"
	"net/url"

	"k8s.io/helm/pkg/downloader"
	"k8s.io/helm/pkg/getter"
	"k8s.io/helm/pkg/helm/helmpath"
	"k8s.io/helm/pkg/helm/environment"
)

// Add with a delay in ... dummy asynch task
func LongtimeAdd(args ...int64) (int64, error) {
	sum := int64(0)
	time.Sleep(1 * time.Second)
	for _, arg := range args {
		sum += arg
	}
	return sum, nil
}

func ChartDownload() (*url.URL, error) {
	c := downloader.ChartDownloader{
		HelmHome: helmpath.Home("/root/.helm"),
		Out:      os.Stderr,
		Getters:  getter.All(environment.EnvSettings{}),
	}
	ref := "mongodb"
	version := "5.17.0"
	u, _, err := c.ResolveChartVersion(ref, version)
	return u, err
}
