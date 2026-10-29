package com.producttracking.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "products")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ToString
@EqualsAndHashCode
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "origin", nullable = false)
    private String origin;

    @Column(name = "status", nullable = false, length = 50)
    @Builder.Default
    private String status = "Manufactured";

    @PrePersist
    public void prePersist() {
        if (this.status == null || this.status.trim().isEmpty()) {
            this.status = "Manufactured";
        }
    }
}
