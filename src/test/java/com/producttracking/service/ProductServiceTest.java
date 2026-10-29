package com.producttracking.service;

import com.producttracking.dto.ProductRequestDto;
import com.producttracking.dto.StatusUpdateDto;
import com.producttracking.entity.Product;
import com.producttracking.exception.ResourceNotFoundException;
import com.producttracking.repository.ProductRepository;
import com.producttracking.service.impl.ProductServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ProductServiceTest {

    @Mock
    private ProductRepository productRepository;

    @InjectMocks
    private ProductServiceImpl productService;

    private Product sampleProduct;

    @BeforeEach
    void setUp() {
        sampleProduct = Product.builder()
                .id(1L)
                .name("Mechanical Keyboard")
                .origin("Assembly Plant 1")
                .status("Manufactured")
                .build();
    }

    @Test
    @DisplayName("getAllProducts returns all products from repository")
    void testGetAllProducts() {
        Product second = Product.builder()
                .id(2L)
                .name("Smart Monitor")
                .origin("Factory B")
                .status("Shipped")
                .build();

        when(productRepository.findAll()).thenReturn(Arrays.asList(sampleProduct, second));

        List<Product> result = productService.getAllProducts();

        assertEquals(2, result.size());
        assertEquals("Mechanical Keyboard", result.get(0).getName());
        verify(productRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("getProductById returns product when found")
    void testGetProductById_Success() {
        when(productRepository.findById(1L)).thenReturn(Optional.of(sampleProduct));

        Product result = productService.getProductById(1L);

        assertNotNull(result);
        assertEquals(1L, result.getId());
        assertEquals("Mechanical Keyboard", result.getName());
    }

    @Test
    @DisplayName("getProductById throws ResourceNotFoundException when not found")
    void testGetProductById_NotFound() {
        when(productRepository.findById(99L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> productService.getProductById(99L));
    }

    @Test
    @DisplayName("createProduct sets default status to Manufactured when status is null or empty")
    void testCreateProduct_DefaultStatus() {
        ProductRequestDto dto = ProductRequestDto.builder()
                .name("Industrial Sensor")
                .origin("Plant Dallas")
                .status(null)
                .build();

        when(productRepository.save(any(Product.class))).thenAnswer(invocation -> {
            Product p = invocation.getArgument(0);
            p.setId(3L);
            return p;
        });

        Product created = productService.createProduct(dto);

        assertNotNull(created);
        assertEquals("Manufactured", created.getStatus());
        assertEquals("Industrial Sensor", created.getName());
        assertEquals("Plant Dallas", created.getOrigin());
    }

    @Test
    @DisplayName("createProduct preserves explicitly provided status")
    void testCreateProduct_CustomStatus() {
        ProductRequestDto dto = ProductRequestDto.builder()
                .name("Industrial Sensor")
                .origin("Plant Dallas")
                .status("Shipped")
                .build();

        when(productRepository.save(any(Product.class))).thenAnswer(invocation -> {
            Product p = invocation.getArgument(0);
            p.setId(3L);
            return p;
        });

        Product created = productService.createProduct(dto);

        assertNotNull(created);
        assertEquals("Shipped", created.getStatus());
    }

    @Test
    @DisplayName("updateProductStatus updates only status, preserving name and origin")
    void testUpdateProductStatus_Success() {
        when(productRepository.findById(1L)).thenReturn(Optional.of(sampleProduct));
        when(productRepository.save(any(Product.class))).thenAnswer(invocation -> invocation.getArgument(0));

        StatusUpdateDto updateDto = StatusUpdateDto.builder()
                .status("Delivered")
                .build();

        Product updated = productService.updateProductStatus(1L, updateDto);

        assertEquals("Delivered", updated.getStatus());
        assertEquals("Mechanical Keyboard", updated.getName());
        assertEquals("Assembly Plant 1", updated.getOrigin());
    }

    @Test
    @DisplayName("updateProductStatus throws ResourceNotFoundException for invalid ID")
    void testUpdateProductStatus_NotFound() {
        when(productRepository.findById(99L)).thenReturn(Optional.empty());

        StatusUpdateDto updateDto = StatusUpdateDto.builder().status("Shipped").build();

        assertThrows(ResourceNotFoundException.class, () -> productService.updateProductStatus(99L, updateDto));
    }

    @Test
    @DisplayName("deleteProduct removes existing product")
    void testDeleteProduct_Success() {
        when(productRepository.findById(1L)).thenReturn(Optional.of(sampleProduct));
        doNothing().when(productRepository).delete(sampleProduct);

        assertDoesNotThrow(() -> productService.deleteProduct(1L));
        verify(productRepository, times(1)).delete(sampleProduct);
    }

    @Test
    @DisplayName("deleteProduct throws ResourceNotFoundException when product does not exist")
    void testDeleteProduct_NotFound() {
        when(productRepository.findById(99L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> productService.deleteProduct(99L));
        verify(productRepository, never()).delete(any());
    }
}
