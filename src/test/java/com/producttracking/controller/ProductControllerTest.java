package com.producttracking.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.producttracking.dto.ProductRequestDto;
import com.producttracking.dto.StatusUpdateDto;
import com.producttracking.entity.Product;
import com.producttracking.exception.ResourceNotFoundException;
import com.producttracking.service.ProductService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;
import java.util.Collections;

import static org.hamcrest.Matchers.hasSize;
import static org.hamcrest.Matchers.is;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class ProductControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private ProductService productService;

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
    @DisplayName("GET /products returns list of products in JSON format")
    void testGetAllProducts() throws Exception {
        Product p2 = Product.builder()
                .id(2L)
                .name("Smart Monitor")
                .origin("Factory B")
                .status("Shipped")
                .build();

        when(productService.getAllProducts()).thenReturn(Arrays.asList(sampleProduct, p2));

        mockMvc.perform(get("/products")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(2)))
                .andExpect(jsonPath("$[0].id", is(1)))
                .andExpect(jsonPath("$[0].name", is("Mechanical Keyboard")))
                .andExpect(jsonPath("$[0].origin", is("Assembly Plant 1")))
                .andExpect(jsonPath("$[0].status", is("Manufactured")))
                .andExpect(jsonPath("$[1].id", is(2)))
                .andExpect(jsonPath("$[1].name", is("Smart Monitor")))
                .andExpect(jsonPath("$[1].origin", is("Factory B")))
                .andExpect(jsonPath("$[1].status", is("Shipped")));
    }

    @Test
    @DisplayName("GET /products/{id} returns single product")
    void testGetProductById() throws Exception {
        when(productService.getProductById(1L)).thenReturn(sampleProduct);

        mockMvc.perform(get("/products/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("Mechanical Keyboard")))
                .andExpect(jsonPath("$.origin", is("Assembly Plant 1")))
                .andExpect(jsonPath("$.status", is("Manufactured")));
    }

    @Test
    @DisplayName("GET /products/{id} returns 404 when product not found")
    void testGetProductById_NotFound() throws Exception {
        when(productService.getProductById(999L))
                .thenThrow(new ResourceNotFoundException("Product not found with id: 999"));

        mockMvc.perform(get("/products/999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status", is(404)))
                .andExpect(jsonPath("$.error", is("Not Found")))
                .andExpect(jsonPath("$.message", is("Product not found with id: 999")));
    }

    @Test
    @DisplayName("POST /products creates and returns product with generated ID")
    void testCreateProduct() throws Exception {
        ProductRequestDto requestDto = ProductRequestDto.builder()
                .name("Industrial Sensor")
                .origin("Plant Dallas")
                .status("Manufactured")
                .build();

        Product created = Product.builder()
                .id(3L)
                .name("Industrial Sensor")
                .origin("Plant Dallas")
                .status("Manufactured")
                .build();

        when(productService.createProduct(any(ProductRequestDto.class))).thenReturn(created);

        mockMvc.perform(post("/products")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(requestDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(3)))
                .andExpect(jsonPath("$.name", is("Industrial Sensor")))
                .andExpect(jsonPath("$.origin", is("Plant Dallas")))
                .andExpect(jsonPath("$.status", is("Manufactured")));
    }

    @Test
    @DisplayName("POST /products with missing fields returns 400 Bad Request")
    void testCreateProduct_ValidationFailure() throws Exception {
        ProductRequestDto invalidDto = ProductRequestDto.builder()
                .name("")
                .origin("   ")
                .build();

        mockMvc.perform(post("/products")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidDto)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status", is(400)))
                .andExpect(jsonPath("$.error", is("Bad Request")));
    }

    @Test
    @DisplayName("PUT /products/{id}/status updates and returns updated product")
    void testUpdateProductStatus() throws Exception {
        StatusUpdateDto updateDto = StatusUpdateDto.builder()
                .status("Shipped")
                .build();

        Product updated = Product.builder()
                .id(1L)
                .name("Mechanical Keyboard")
                .origin("Assembly Plant 1")
                .status("Shipped")
                .build();

        when(productService.updateProductStatus(eq(1L), any(StatusUpdateDto.class))).thenReturn(updated);

        mockMvc.perform(put("/products/1/status")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updateDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.status", is("Shipped")))
                .andExpect(jsonPath("$.name", is("Mechanical Keyboard")))
                .andExpect(jsonPath("$.origin", is("Assembly Plant 1")));
    }

    @Test
    @DisplayName("PUT /products/{id}/status with blank status returns 400 Bad Request")
    void testUpdateProductStatus_ValidationFailure() throws Exception {
        StatusUpdateDto invalidDto = StatusUpdateDto.builder()
                .status("   ")
                .build();

        mockMvc.perform(put("/products/1/status")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidDto)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status", is(400)));
    }

    @Test
    @DisplayName("PUT /products/{id}/status with non-existent ID returns 404")
    void testUpdateProductStatus_NotFound() throws Exception {
        StatusUpdateDto updateDto = StatusUpdateDto.builder().status("Delivered").build();

        when(productService.updateProductStatus(eq(999L), any(StatusUpdateDto.class)))
                .thenThrow(new ResourceNotFoundException("Product not found with id: 999"));

        mockMvc.perform(put("/products/999/status")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updateDto)))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status", is(404)));
    }

    @Test
    @DisplayName("PUT /products/{id}/status with non-numeric ID returns 400 Bad Request")
    void testUpdateProductStatus_InvalidIdFormat() throws Exception {
        StatusUpdateDto updateDto = StatusUpdateDto.builder().status("Shipped").build();

        mockMvc.perform(put("/products/abc/status")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updateDto)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status", is(400)));
    }

    @Test
    @DisplayName("DELETE /products/{id} deletes existing product")
    void testDeleteProduct_Success() throws Exception {
        doNothing().when(productService).deleteProduct(1L);

        mockMvc.perform(delete("/products/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message", is("Product deleted successfully")));

        verify(productService, times(1)).deleteProduct(1L);
    }

    @Test
    @DisplayName("DELETE /products/{id} returns 404 when product not found")
    void testDeleteProduct_NotFound() throws Exception {
        doThrow(new ResourceNotFoundException("Product not found with id: 999"))
                .when(productService).deleteProduct(999L);

        mockMvc.perform(delete("/products/999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status", is(404)));
    }
}
