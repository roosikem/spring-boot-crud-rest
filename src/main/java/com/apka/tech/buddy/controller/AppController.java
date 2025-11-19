package com.apka.tech.buddy.controller;

import com.apka.tech.buddy.model.dto.AppDTO;
import com.apka.tech.buddy.service.AppService;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.util.UriComponents;
import org.springframework.web.util.UriComponentsBuilder;

import jakarta.validation.Valid;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/apps")
public class AppController {

    private final AppService service;

    @PostMapping
    public ResponseEntity<?> create(@Valid @RequestBody AppDTO dto, UriComponentsBuilder uriComponentsBuilder) {
        Long appId = service.createNewApp(dto);
        UriComponents uriComponents = uriComponentsBuilder
            .path("/api/v1/apps/{id}")
            .buildAndExpand(appId);

        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(uriComponents.toUri());

        return new ResponseEntity<>(headers, HttpStatus.CREATED);
    }


}
