package com.apka.tech.buddy.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;

@Data
@NoArgsConstructor
public class AppDTO {

    @NotEmpty
    @Size(max = 20)
    @JsonProperty("appName")
    private String name;

    @NotEmpty
    @JsonProperty("appVersion")
    private String version;

    @NotEmpty
    @JsonProperty("devName")
    private String author;

    @Builder
    public AppDTO(String name, String version, String author) {
        this.name = name;
        this.version = version;
        this.author = author;
    }
}
