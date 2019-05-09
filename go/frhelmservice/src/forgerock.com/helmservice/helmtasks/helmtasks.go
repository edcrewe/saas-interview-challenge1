package helmtasks

import (
	"time"
	"os"
	"path/filepath"
	"io/ioutil"

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

func ChartDownload() (string, error) {
	hh := helmpath.Home("/root/.helm")
	c := downloader.ChartDownloader{
		HelmHome: hh,
		Out:      os.Stderr,
		Getters:  getter.All(environment.EnvSettings{}),
	}
	ref := "https://kubernetes-charts.storage.googleapis.com/mongdb"
	version := "5.17.0"
        dest := filepath.Join(hh.String(), "dest")
	_ = os.Mkdir(dest, 0700)
	_, _, err := c.DownloadTo(ref, version, dest)
	contents, err := ioutil.ReadFile(filepath.Join(dest, "mongodb"))
	if err != nil {
		panic(err)
	}
	return string(contents), err
}
