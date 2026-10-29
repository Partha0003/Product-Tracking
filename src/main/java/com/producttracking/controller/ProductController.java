package com.producttracking.controller;

import com.producttracking.dto.ProductRequestDto;
import com.producttracking.dto.StatusUpdateDto;
import com.producttracking.entity.Product;
import com.producttracking.service.ProductService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Collections;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/products")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping
    public ResponseEntity<List<Product>> getAllProducts() {
        List<Product> products = productService.getAllProducts();
        return ResponseEntity.ok(products);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Product> getProductById(@PathVariable Long id) {
        Product product = productService.getProductById(id);
        return ResponseEntity.ok(product);
    }

    @PostMapping
    public ResponseEntity<Product> createProduct(@Valid @RequestBody ProductRequestDto requestDto) {
        Product createdProduct = productService.createProduct(requestDto);
        return ResponseEntity.ok(createdProduct);
    }

    @PutMapping("/{id}/status")
    public ResponseEntity<Product> updateProductStatus(
            @PathVariable Long id,
            @Valid @RequestBody StatusUpdateDto statusDto) {
        Product updatedProduct = productService.updateProductStatus(id, statusDto);
        return ResponseEntity.ok(updatedProduct);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, Object>> deleteProduct(@PathVariable Long id) {
        productService.deleteProduct(id);
        return ResponseEntity.ok(Collections.singletonMap("message", "Product deleted successfully"));
    }
}
