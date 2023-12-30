package main

import (
	"fmt"
	"os"
)

func main() {
	res, _ := os.ReadFile("/flag")
	fmt.Print(string(res))
}
