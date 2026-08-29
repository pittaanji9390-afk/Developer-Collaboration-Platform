package com.forgehub.shared.exception;

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
