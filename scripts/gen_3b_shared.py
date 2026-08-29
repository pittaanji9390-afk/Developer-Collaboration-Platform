from common_writer import write_file

api_resp = """package com.forgehub.shared.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ApiResponse<T> {
    @Builder.Default
    private boolean success = true;
    private String message;
    private T data;
    @Builder.Default
    private Instant timestamp = Instant.now();

    public static <T> ApiResponse<T> ok(T data) {
        return ApiResponse.<T>builder().success(true).data(data).build();
    }

    public static <T> ApiResponse<T> ok(String message, T data) {
        return ApiResponse.<T>builder().success(true).message(message).data(data).build();
    }

    public static <T> ApiResponse<T> ofMessage(String message) {
        return ApiResponse.<T>builder().success(true).message(message).build();
    }
}
"""
write_file("backend/src/main/java/com/forgehub/shared/dto/ApiResponse.java", api_resp)

page_resp = """package com.forgehub.shared.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.domain.Page;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PageResponse<T> {
    private List<T> items;
    private int page;
    private int size;
    private long totalElements;
    private int totalPages;
    private boolean isFirst;
    private boolean isLast;
    private boolean hasNext;
    private boolean hasPrevious;

    public static <T> PageResponse<T> from(Page<T> page) {
        return PageResponse.<T>builder()
                .items(page.getContent())
                .page(page.getNumber())
                .size(page.getSize())
                .totalElements(page.getTotalElements())
                .totalPages(page.getTotalPages())
                .isFirst(page.isFirst())
                .isLast(page.isLast())
                .hasNext(page.hasNext())
                .hasPrevious(page.hasPrevious())
                .build();
    }
}
"""
write_file("backend/src/main/java/com/forgehub/shared/dto/PageResponse.java", page_resp)

err_resp = """package com.forgehub.shared.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse {
    @Builder.Default
    private Instant timestamp = Instant.now();
    private String requestId;
    private int status;
    private String code;
    private String message;
    private List<FieldErrorItem> fieldErrors;

    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    public static class FieldErrorItem {
        private String field;
        private String message;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/shared/dto/ErrorResponse.java", err_resp)

exc_java = """package com.forgehub.shared.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
public class ApiException extends RuntimeException {
    private final HttpStatus status;
    private final String code;

    public ApiException(String message, HttpStatus status, String code) {
        super(message);
        this.status = status;
        this.code = code;
    }

    public static ApiException notFound(String message) {
        return new ApiException(message, HttpStatus.NOT_FOUND, "RESOURCE_NOT_FOUND");
    }

    public static ApiException badRequest(String message) {
        return new ApiException(message, HttpStatus.BAD_REQUEST, "BAD_REQUEST");
    }

    public static ApiException forbidden(String message) {
        return new ApiException(message, HttpStatus.FORBIDDEN, "FORBIDDEN");
    }

    public static ApiException unauthorized(String message) {
        return new ApiException(message, HttpStatus.UNAUTHORIZED, "UNAUTHORIZED");
    }

    public static ApiException conflict(String message) {
        return new ApiException(message, HttpStatus.CONFLICT, "CONFLICT");
    }
}
"""
write_file("backend/src/main/java/com/forgehub/shared/exception/ApiException.java", exc_java)

glob_exc = """package com.forgehub.shared.exception;

import com.forgehub.shared.dto.ErrorResponse;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.List;
import java.util.UUID;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ApiException.class)
    public ResponseEntity<ErrorResponse> handleApiException(ApiException ex, HttpServletRequest request) {
        String reqId = UUID.randomUUID().toString();
        log.warn("API Exception [reqId: {}]: {} - {}", reqId, ex.getCode(), ex.getMessage());
        return ResponseEntity.status(ex.getStatus()).body(
                ErrorResponse.builder()
                        .requestId(reqId)
                        .status(ex.getStatus().value())
                        .code(ex.getCode())
                        .message(ex.getMessage())
                        .build()
        );
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException ex) {
        String reqId = UUID.randomUUID().toString();
        List<ErrorResponse.FieldErrorItem> fieldErrors = ex.getBindingResult().getFieldErrors().stream()
                .map(err -> new ErrorResponse.FieldErrorItem(err.getField(), err.getDefaultMessage()))
                .toList();

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                ErrorResponse.builder()
                        .requestId(reqId)
                        .status(HttpStatus.BAD_REQUEST.value())
                        .code("VALIDATION_ERROR")
                        .message("Request parameter validation failed")
                        .fieldErrors(fieldErrors)
                        .build()
        );
    }

    @ExceptionHandler(BadCredentialsException.class)
    public ResponseEntity<ErrorResponse> handleBadCredentials(BadCredentialsException ex) {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(
                ErrorResponse.builder()
                        .requestId(UUID.randomUUID().toString())
                        .status(HttpStatus.UNAUTHORIZED.value())
                        .code("INVALID_CREDENTIALS")
                        .message("Invalid username or password")
                        .build()
        );
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> handleAccessDenied(AccessDeniedException ex) {
        return ResponseEntity.status(HttpStatus.FORBIDDEN).body(
                ErrorResponse.builder()
                        .requestId(UUID.randomUUID().toString())
                        .status(HttpStatus.FORBIDDEN.value())
                        .code("ACCESS_DENIED")
                        .message("You do not have sufficient permissions to perform this action")
                        .build()
        );
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex) {
        String reqId = UUID.randomUUID().toString();
        log.error("Unhandled server error [reqId: {}]", reqId, ex);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(
                ErrorResponse.builder()
                        .requestId(reqId)
                        .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
                        .code("INTERNAL_SERVER_ERROR")
                        .message("An unexpected internal error occurred. Please contact support.")
                        .build()
        );
    }
}
"""
write_file("backend/src/main/java/com/forgehub/shared/exception/GlobalExceptionHandler.java", glob_exc)

print("gen_3b_shared complete.")