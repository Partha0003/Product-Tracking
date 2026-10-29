package com.producttracking.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RootController {

    @GetMapping(value = "/", produces = "text/plain")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("Server is running!");
    }
}
