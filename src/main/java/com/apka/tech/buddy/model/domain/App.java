package com.apka.tech.buddy.model.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Entity
@NoArgsConstructor
@Table(name = "applications")
public class App {

  @Id
  @GeneratedValue
  private Long id;
  private String author;
  private String name;
  private String version;

  @Builder
  public App(Long id, String author, String name, String version) {
    this.id = id;
    this.author = author;
    this.name = name;
    this.version = version;
  }

}
