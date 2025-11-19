package com.apka.tech.buddy.service.impl;

import com.apka.tech.buddy.builder.AppBuilder;
import com.apka.tech.buddy.exception.AppNotFoundException;
import com.apka.tech.buddy.model.domain.App;
import com.apka.tech.buddy.model.dto.AppDTO;
import com.apka.tech.buddy.repository.AppRepository;
import com.apka.tech.buddy.service.AppService;
import com.github.javafaker.Faker;
import lombok.AllArgsConstructor;
import lombok.val;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

@Service
@AllArgsConstructor
public class AppServiceImpl implements AppService {

    private final AppRepository repository;
    private final AppBuilder builder;

    @Override
    public Long createNewApp(AppDTO dto) {
        return Stream.of(dto)
            .map(builder::build)
            .map(repository::save)
            .map(App::getId)
            .findFirst()
            .get();
    }

}
