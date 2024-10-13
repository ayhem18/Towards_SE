package utils

import (
	"path"
	"strings"
)


func GetPathBasename(file_path string) string {
	file_path = strings.ReplaceAll(file_path, "\\", "//")
	return path.Base(file_path)
}
