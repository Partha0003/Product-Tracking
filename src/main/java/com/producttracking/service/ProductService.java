package com.producttracking.service;

import com.producttracking.dto.ProductRequestDto;
import com.producttracking.dto.StatusUpdateDto;
import com.producttracking.entity.Product;

import java.util.List;

public interface ProductService {

    List<Product> getAllProducts();

    Product getProductById(Long id);

    Product createProduct(ProductRequestDto dto);

    Product updateProductStatus(Long id, StatusUpdateDto dto);

    void deleteProduct(Long id);
}
