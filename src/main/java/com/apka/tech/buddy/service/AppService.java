package com.apka.tech.buddy.service;

import java.util.List;
import java.util.Optional;

import com.apka.tech.buddy.model.dto.AppDTO;

public interface AppService {

    Long createNewApp(AppDTO dto);

}
