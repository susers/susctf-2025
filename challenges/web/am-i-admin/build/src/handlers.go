package main

import (
	"encoding/json"
	"net/http"
	"os/exec"
)

type RunCommandReq struct {
	Cmd  string   `json:"cmd"`
	Args []string `json:"args"`
}

func RunCommandHandler(w http.ResponseWriter, r *http.Request) {
	var body RunCommandReq
	json.NewDecoder(r.Body).Decode(&body)
	out, err := exec.Command(body.Cmd, body.Args...).CombinedOutput()
	resp := map[string]string{
		"output": string(out),
	}
	if err != nil {
		resp["error"] = err.Error()
	}
	json.NewEncoder(w).Encode(resp)
}
