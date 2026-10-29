package com.producttracking.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ToString
public class ProductRequestDto {

    @NotBlank(message = "Product name is required and cannot be blank")
    private String name;

    @NotBlank(message = "Product origin is required and cannot be blank")
    private String origin;

    private String status;
}
