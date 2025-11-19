package com.apka.tech.buddy.utils;

import com.apka.tech.buddy.model.dto.AppDTO;

public class AppUtils {

    public static AppDTO createAppDto(String name, String version, String author) {
        return AppDTO.builder()
            .name(name)
            .version(version)
            .author(author)
            .build();
    }
}
