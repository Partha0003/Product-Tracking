package com.producttracking.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ToString
public class StatusUpdateDto {

    @NotBlank(message = "Status is required and cannot be blank")
    private String status;
}
