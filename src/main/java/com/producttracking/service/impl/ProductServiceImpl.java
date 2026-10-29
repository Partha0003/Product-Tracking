package com.producttracking.service.impl;

import com.producttracking.dto.ProductRequestDto;
import com.producttracking.dto.StatusUpdateDto;
import com.producttracking.entity.Product;
import com.producttracking.exception.ResourceNotFoundException;
import com.producttracking.repository.ProductRepository;
import com.producttracking.service.ProductService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional
public class ProductServiceImpl implements ProductService {

    private final ProductRepository productRepository;

    public ProductServiceImpl(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }

    @Override
    @Transactional(readOnly = true)
    public Product getProductById(Long id) {
        return productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
    }

    @Override
    public Product createProduct(ProductRequestDto dto) {
        String status = (dto.getStatus() != null && !dto.getStatus().trim().isEmpty())
                ? dto.getStatus().trim()
                : "Manufactured";

        Product product = Product.builder()
                .name(dto.getName().trim())
                .origin(dto.getOrigin().trim())
                .status(status)
                .build();

        return productRepository.save(product);
    }

    @Override
    public Product updateProductStatus(Long id, StatusUpdateDto dto) {
        Product existingProduct = productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));

        // Update ONLY the status; name and origin are strictly protected
        existingProduct.setStatus(dto.getStatus().trim());

        return productRepository.save(existingProduct);
    }

    @Override
    public void deleteProduct(Long id) {
        Product existingProduct = productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));

        productRepository.delete(existingProduct);
    }
}
