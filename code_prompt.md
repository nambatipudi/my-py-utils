# 📦 Collected Source Files

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/CncItcApplicationTest.java`

```java
package com.vertex.cnc.itc;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Configuration;
import org.springframework.test.context.ActiveProfiles;

import static com.vertex.cnc.itc.common.constants.ApplicationConstants.TEST_PROFILE;

@SpringBootTest(classes = CncItcApiApplication.class)
@ActiveProfiles(TEST_PROFILE)
class CncItcApplicationTest {

	@Configuration
	static class TestConfig {

	}

	@Test
	void contextLoads() {
		assert (true);
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/common/WebClientUtilsTest.java`

```java
package com.vertex.cnc.itc.common;

import com.vertex.cnc.itc.common.exception.ApiException;
import com.vertex.cnc.itc.common.utility.WebClientUtils;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class WebClientUtilsTest {

    @Mock
    private RestTemplate restTemplate;

    private WebClientUtils webClientUtils;

    private String token;
    private String uri;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        webClientUtils = new WebClientUtils(restTemplate);
        token = "Bearer test-token";
        uri = "http://example.com/api/resource";
    }

    @Test
    public void testPerformRestGet_Success() {
        // Arrange
        ParameterizedTypeReference<String> responseType = new ParameterizedTypeReference<>() {};
        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
        headers.add(HttpHeaders.AUTHORIZATION, token);
        HttpEntity<String> httpEntity = new HttpEntity<>(null, headers);

        ResponseEntity<String> responseEntity = new ResponseEntity<>("Success Response", HttpStatus.OK);
        when(restTemplate.exchange(uri, HttpMethod.GET, httpEntity, responseType)).thenReturn(responseEntity);

        // Act
        String result = webClientUtils.performRestGet(token, uri, responseType);

        // Assert
        assertEquals("Success Response", result);
        verify(restTemplate, times(1)).exchange(uri, HttpMethod.GET, httpEntity, responseType);
    }

    @Test
    public void testPerformRestGet_NoResponseBody() {
        // Arrange
        ParameterizedTypeReference<String> responseType = new ParameterizedTypeReference<>() {};
        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
        headers.add(HttpHeaders.AUTHORIZATION, token);
        HttpEntity<String> httpEntity = new HttpEntity<>(null, headers);

        ResponseEntity<String> responseEntity = new ResponseEntity<>(null, new HttpHeaders(), HttpStatus.OK);
        when(restTemplate.exchange(uri, HttpMethod.GET, httpEntity, responseType)).thenReturn(responseEntity);

        // Act & Assert
        ApiException exception = assertThrows(ApiException.class, () -> {
            webClientUtils.performRestGet(token, uri, responseType);
        });
        assertEquals("Did not get a body in the response.", exception.getMessage());
        verify(restTemplate, times(1)).exchange(uri, HttpMethod.GET, httpEntity, responseType);
    }

    @Test
    public void testPerformRestGet_RestClientException() {
        // Arrange
        ParameterizedTypeReference<String> responseType = new ParameterizedTypeReference<>() {};
        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
        headers.add(HttpHeaders.AUTHORIZATION, token);
        HttpEntity<String> httpEntity = new HttpEntity<>(null, headers);

        when(restTemplate.exchange(uri, HttpMethod.GET, httpEntity, responseType))
                .thenThrow(new RestClientException("Test RestClientException"));

        // Act & Assert
        RestClientException exception = assertThrows(RestClientException.class, () -> {
            webClientUtils.performRestGet(token, uri, responseType);
        });
        assertEquals("Test RestClientException", exception.getMessage());
        verify(restTemplate, times(1)).exchange(uri, HttpMethod.GET, httpEntity, responseType);
    }
}
```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/security/configuration/OAuth2ResourceServerSecurityConfigurationTest.java`

```java
package com.vertex.cnc.itc.security.configuration;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.CorsConfigurer;
import org.springframework.security.config.annotation.web.configurers.oauth2.server.resource.OAuth2ResourceServerConfigurer;
import org.springframework.security.oauth2.server.resource.authentication.JwtIssuerAuthenticationManagerResolver;

import java.lang.reflect.Field;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class OAuth2ResourceServerSecurityConfigurationTest {

	@Mock
	private HttpSecurity http;

	@Mock
	private CorsConfigurer cors;

	@Mock
	private OAuth2ResourceServerConfigurer oauth;

	@Mock
	private JwtIssuerAuthenticationManagerResolver resolver;

	@InjectMocks
	private OAuth2ResourceServerSecurityConfiguration config;

	@Mock
	private OAuth2ResourceServerConfigurer oauth1;

	private String vertexIssuer;

	private String auth0Issuer;

	@BeforeEach
	void setUp() throws Exception {
		vertexIssuer = "https://devauth.vertexsmb.com/identity";
		auth0Issuer = "https://dev-auth.vtxdev.net/";

		setField(config, "vertexIssuer", vertexIssuer);
		setField(config, "auth0Issuer", auth0Issuer);
		setField(config, "cncScopeSecurity", "some-scope");

	}

	@Test
	void testConfigure() throws Exception {
		when(http.cors(Customizer.withDefaults())).thenReturn(http);
		when(http.authorizeHttpRequests(any())).thenReturn(http);
		when(http.oauth2ResourceServer(any())).thenReturn(http);
		when(http.oauth2ResourceServer(any())).thenReturn(http);
		when(http.csrf(any())).thenReturn(http);
		config.filterChain(http);
		verify(http, times(1)).cors(Customizer.withDefaults());
		verify(http, times(2)).authorizeHttpRequests(any());
		verify(http, times(1)).oauth2ResourceServer(any());
		verify(http, times(1)).csrf(any());
	}

	private void setField(Object target, String fieldName, Object value) throws Exception {
		Field field = target.getClass().getDeclaredField(fieldName);
		field.setAccessible(true);
		field.set(target, value);
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/security/controller/PermissionControllerImplTest.java`

```java
package com.vertex.cnc.itc.security.controller;

import com.vertex.cnc.itc.security.dto.UserAccessPermissionResponseDTO;
import com.vertex.cnc.itc.security.service.PermissionService;
import com.vertex.cnc.itc.security.controller.impl.PermissionControllerImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class PermissionControllerImplTest {

    @Mock
    private PermissionService permissionService;

    private PermissionControllerImpl permissionController;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        permissionController = new PermissionControllerImpl(permissionService);
    }

    @Test
    public void testGetUserAccessPermissions_Success() {
        // Arrange
        List<UserAccessPermissionResponseDTO> expectedPermissions = Arrays.asList(
                new UserAccessPermissionResponseDTO(),
                new UserAccessPermissionResponseDTO()
        );
        when(permissionService.getUserAccessPermissions()).thenReturn(expectedPermissions);

        // Act
        List<UserAccessPermissionResponseDTO> actualPermissions = permissionController.getUserAccessPermissions();

        // Assert
        assertEquals(expectedPermissions, actualPermissions);
        verify(permissionService, times(1)).getUserAccessPermissions();
    }

    @Test
    public void testGetUserAccessPermissions_NullService() {
        // Arrange
        PermissionControllerImpl controllerWithNullService = new PermissionControllerImpl(null);

        // Act
        List<UserAccessPermissionResponseDTO> permissions = controllerWithNullService.getUserAccessPermissions();

        // Assert
        assertNull(permissions);
    }

    @Test
    public void testGetUserAccessPermissions_ExceptionThrown() {
        // Arrange
        when(permissionService.getUserAccessPermissions()).thenThrow(new RuntimeException("Test exception"));

        // Act & Assert
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            permissionController.getUserAccessPermissions();
        });
        assertEquals("Test exception", exception.getMessage());
        verify(permissionService, times(1)).getUserAccessPermissions();
    }
}
```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/configuration/TestApplicationFilter.java`

```java
package com.vertex.cnc.itc.configuration;

import com.vertex.cnc.itc.common.aop.CNCITCContext;
import com.vertex.cnc.itc.security.dto.*;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.mockito.MockedStatic;
import org.springframework.boot.test.context.TestComponent;
import org.springframework.context.annotation.Primary;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;

import static org.mockito.Mockito.mockStatic;
import static org.mockito.Mockito.withSettings;

@TestComponent
@Primary
public class TestApplicationFilter extends OncePerRequestFilter {

	private static Role testRole;

	public static void setTestRole(Role role) {
		testRole = role;
	}

	@Override
	protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
			throws ServletException, IOException {
		try (MockedStatic<CNCITCContext> mockedStaticMethod = mockStatic(CNCITCContext.class,
				withSettings().verboseLogging())) {

			CNCITCContext context = initializeContext(request);
			mockedStaticMethod.when(CNCITCContext::getContext).thenReturn(context);

			filterChain.doFilter(request, response);
		}
	}

	private CNCITCContext initializeContext(HttpServletRequest request) {
		UserProfile userProfile = new UserProfile();
		userProfile.setSub(request.getParameter("userSub") != null ? request.getParameter("userSub") : "defaultSub");

		Feature feature = new Feature("tta-ind-tax-close", "370", "TTA - Indirect Tax Close");
		Subscription subscription = new Subscription();
		subscription.setFeatures(List.of(feature));

		TenantProfile tenantProfile = new TenantProfile();
		tenantProfile.setTenantId("tenantId");
		tenantProfile.setRoles(List.of(testRole));
		tenantProfile.setSubscription(subscription);

		CNCITCContext context = new CNCITCContext();
		context.setUserProfile(userProfile);
		context.setTenantProfile(tenantProfile);
		context.setRole(testRole);
		context.setFeatures(List.of(feature));

		return context;
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/configuration/SpringDocConfigurationTest.java`

```java
package com.vertex.cnc.itc.configuration;

import io.swagger.v3.oas.models.OpenAPI;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.assertNotNull;

@ExtendWith(MockitoExtension.class)
class SpringDocConfigurationTest {

	@InjectMocks
	private SpringDocConfiguration configuration;

	@Test
	void testCustomOpenAPI() {
		OpenAPI openApi = configuration.springDocOpenAPI();
		assertNotNull(openApi, "configuration should generate a custom open api object");
	}

}
```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/configuration/ApiExceptionHandlerTest.java`

```java
package com.vertex.cnc.itc.configuration;

import com.vertex.cnc.itc.common.exception.ApiException;
import com.vertex.cnc.itc.common.exception.UnauthorizedAccessException;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.context.request.WebRequest;

import java.sql.SQLException;

import static org.junit.jupiter.api.Assertions.assertEquals;

@ExtendWith(MockitoExtension.class)
class ApiExceptionHandlerTest {

	@Mock
	private HttpHeaders httpHeaders;

	@Mock
	private WebRequest webRequest;

	private ApiExceptionHandler apiExceptionHandler = new ApiExceptionHandler();

	@Test
	void testHandleAccessDeniedExceptions() {
		AccessDeniedException exception = new AccessDeniedException("test");
		ResponseEntity<Object> responseEntity = apiExceptionHandler.handleAccessDeniedExceptions(exception);
		assertEquals(HttpStatus.FORBIDDEN, responseEntity.getStatusCode(), "status code should be 403");
	}

	@Test
	void testHandleAllExceptions() {
		Exception exception = new Exception("test");
		ResponseEntity<Object> responseEntity = apiExceptionHandler.handleAllExceptions(exception);
		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, responseEntity.getStatusCode(), "status code should be 500");
	}

	@Test
	void testHandleReportApiException() {
		ApiException exception = new ApiException(HttpStatus.BAD_REQUEST, "test");
		ResponseEntity<Object> responseEntity = apiExceptionHandler.handleReportApiException(exception);
		assertEquals(HttpStatus.BAD_REQUEST, responseEntity.getStatusCode(), "status code should be 400");
	}

	@Test
	void testHandleDataIntegrityViolationException() {
		DataIntegrityViolationException exception = new DataIntegrityViolationException("test", new SQLException());
		ResponseEntity<Object> responseEntity = apiExceptionHandler.handleDataIntegrityViolationException(exception);
		assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, responseEntity.getStatusCode(), "status code should be 500");
	}

	@Test
	void testHandleEmptyResultDataAccessException() {
		EmptyResultDataAccessException exception = new EmptyResultDataAccessException("some task", 1,
				new SQLException());
		ResponseEntity<Object> responseEntity = apiExceptionHandler.handleEmptyResultDataAccessException(exception);
		assertEquals(HttpStatus.NO_CONTENT, responseEntity.getStatusCode(), "status code should be 204");
	}

	@Test
	void testHandleUnauthorizedAccessException() {
		UnauthorizedAccessException exception = new UnauthorizedAccessException("test");
		ResponseEntity<Object> responseEntity = apiExceptionHandler.handleUnauthorizedAccessException(exception);
		assertEquals(HttpStatus.UNAUTHORIZED, responseEntity.getStatusCode(), "status code should be 401");
	}

}
```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/configuration/SecurityTestConfig.java`

```java
package com.vertex.cnc.itc.configuration;

import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@TestConfiguration
public class SecurityTestConfig {

	@Bean
	public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
		http.authorizeHttpRequests(authorize -> authorize.anyRequest().permitAll());
		http.oauth2ResourceServer(oauth2 -> oauth2.disable());
		http.csrf(csrf -> csrf.disable());
		return http.build();
	}

}
```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/datareadiness/dao/EntityDaoImplTest.java`

```java
package com.vertex.cnc.itc.datareadiness.dao;

import com.vertex.cnc.itc.datareadiness.configuration.EntityListQueryConfiguration;
import com.vertex.cnc.itc.datareadiness.dao.impl.EntityDaoImpl;

import com.vertex.cnc.itc.datareadiness.dto.request.EntityRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessSummaryResponseDTO;
import com.vertex.cnc.itc.datareadiness.mapper.EntityDataReadinessSummaryDTORowMapper;
import com.vertex.cnc.itc.datareadiness.response.DataReadinessSummary;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.core.env.Environment;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;

import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class EntityDaoImplTest {

    @Mock
    private NamedParameterJdbcTemplate namedParameterJdbcTemplate;

    @Mock
    private EntityDataReadinessSummaryDTORowMapper entityDataReadinessSummaryDTORowMapper;

    @Mock
    private EntityListQueryConfiguration entityListQueryConfiguration;

    @Mock
    private Environment environment;

    @InjectMocks
    private EntityDaoImpl entityDaoImpl;

    @Test
    public void testGetTenantEntities() {
        EntityRequestDTO request = new EntityRequestDTO();
        request.setStartDate(ZonedDateTime.parse("2024-01-01T05:00:00Z"));
        request.setEndDate(ZonedDateTime.parse("2024-01-31T05:00:00Z"));
        request.setPeriodId("periodId");
        String tenantId = "testTenantId";

        List<EntityDataReadinessSummaryResponseDTO> expectedResponse = new ArrayList<>();
        EntityDataReadinessSummaryResponseDTO listItem =
                new EntityDataReadinessSummaryResponseDTO();
        listItem.setEntityId("entityId");
        listItem.setDataReadinessStatus("Validated Data");
        expectedResponse.add(listItem);

		when(environment.getActiveProfiles()).thenReturn(new String[]{"testProfile", "testProfile2"});
        when(entityListQueryConfiguration.getEntityListQuery())
                .thenReturn("entityListQuery");
		when(namedParameterJdbcTemplate.queryForObject(anyString(), anyMap(),
				any(EntityDataReadinessSummaryDTORowMapper.class))).thenReturn(expectedResponse);


		DataReadinessSummary result = entityDaoImpl.getTenantEntities(request, tenantId);

        assertNotNull(result);
        assertEquals(1, result.getEntityDataReadinessSummaries().size());
        assertEquals(1, result.getStatusCounts().get("Validated Data"));
        assertEquals(0, result.getStatusCounts().get("Needs Review"));
        assertEquals(0, result.getStatusCounts().get("Not Ready"));
    }

    @Test
    public void testGetTenantEntitiesNoDataFound() {
        EntityRequestDTO request = new EntityRequestDTO();
        request.setStartDate(ZonedDateTime.parse("2024-01-01T05:00:00Z"));
        request.setEndDate(ZonedDateTime.parse("2024-01-31T05:00:00Z"));
        request.setPeriodId("periodId");
        String tenantId = "testTenantId";

        List<EntityDataReadinessSummaryResponseDTO> expectedResponse = new ArrayList<>();

		when(environment.getActiveProfiles()).thenReturn(new String[]{"testProfile", "testProfile2"});
        when(entityListQueryConfiguration.getEntityListQuery())
                .thenReturn("entityListQuery");
		when(namedParameterJdbcTemplate.queryForObject(anyString(), anyMap(),
				any(EntityDataReadinessSummaryDTORowMapper.class))).thenReturn(expectedResponse);

        DataReadinessSummary result = entityDaoImpl.getTenantEntities(request, tenantId);

        assertNotNull(result);
        assertEquals(0, result.getEntityDataReadinessSummaries().size());
        assertEquals(0, result.getStatusCounts().get("Validated Data"));
        assertEquals(0, result.getStatusCounts().get("Needs Review"));
        assertEquals(0, result.getStatusCounts().get("Not Ready"));
    }

    @Test
    public void testLoadClientEntityPeriodItcStatus() {
        Map<String, Object> params = new HashMap<>();
        when(environment.getActiveProfiles()).thenReturn(new String[]{"testProfile", "testProfile2"});
        when(entityListQueryConfiguration.getClientEntityPeriodStatusQuery())
                .thenReturn("entityListQuery");
        entityDaoImpl.loadClientEntityPeriodItcStatus();

        verify(namedParameterJdbcTemplate).update("entityListQuery", params);
    }

}

```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/datareadiness/dao/EntityDataReadinessDetailsDaoImplTest.java`

```java
package com.vertex.cnc.itc.datareadiness.dao;

import com.vertex.cnc.itc.datareadiness.configuration.EntityDetailsQueryConfiguration;
import com.vertex.cnc.itc.datareadiness.dao.impl.EntityDataReadinessDetailsDaoImpl;
import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessDetailsDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityDetailsRequestDTO;
import com.vertex.cnc.itc.datareadiness.mapper.TransactionDetailsRowMapper;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessDetails;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.core.env.Environment;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;

import java.time.ZonedDateTime;
import java.util.*;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class EntityDataReadinessDetailsDaoImplTest {
    @Mock
    private NamedParameterJdbcTemplate namedParameterJdbcTemplate;

    @Mock
    private TransactionDetailsRowMapper transactionDetailsRowMapper;

    @Mock
    private EntityDetailsQueryConfiguration entityDetailsQueryConfiguration;

    @InjectMocks
    private EntityDataReadinessDetailsDaoImpl entityDataReadinessDetailsDaoImpl;

	@Mock
	private Environment environment;

    @BeforeEach
    public void setUp() {
     when(environment.getActiveProfiles()).thenReturn(new String[]{"test"});
	 when(entityDetailsQueryConfiguration.getEntityTransactionDetailsQuery()).thenReturn("Query");
    }

    @Test
    public void testGetEntityDetailsResponse() {
        EntityDetailsRequestDTO request = new EntityDetailsRequestDTO ();
        request.setStartDate(ZonedDateTime.parse("2024-01-01T05:00:00Z"));
        request.setEndDate(ZonedDateTime.parse("2024-01-31T05:00:00Z"));
        String tenantId = "testTenantId";
        String entityId = "testEntityId";
        request.setEntityId(entityId);

        List<EntityDataReadinessDetailsDTO> expectedResponse = new ArrayList<>();
        EntityDataReadinessDetailsDTO transaction1 = EntityDataReadinessDetailsDTO.builder()
                .tenantId(tenantId)
                .transactionIdCode("TXN123")
                .lineItemIdCode("LINE001")
                .lineItemNumber("1")
                .postingDate("2024-01-05")
                .dfIsProcessed(1)
                .processingMessage("Processed successfully")
                .build();

        EntityDataReadinessDetailsDTO transaction2 = EntityDataReadinessDetailsDTO.builder()
                .tenantId(tenantId)
                .transactionIdCode("TXN124")
                .lineItemIdCode("LINE002")
                .lineItemNumber("2")
                .postingDate("2024-01-10")
                .dfIsProcessed(0)
                .processingMessage("Processing failed")
                .build();

        // add couple of null transactionidcode - these 2 will be counted as 1 transaction
        EntityDataReadinessDetailsDTO transaction3 = EntityDataReadinessDetailsDTO.builder()
                .tenantId(tenantId)
                .transactionIdCode(null)
                .dfIsProcessed(1)
                .build();

        EntityDataReadinessDetailsDTO transaction4 = EntityDataReadinessDetailsDTO.builder()
                .tenantId(tenantId)
                .transactionIdCode(null)
                .dfIsProcessed(0)
                .build();

        expectedResponse.add(transaction1);
        expectedResponse.add(transaction2);
        expectedResponse.add(transaction3);
        expectedResponse.add(transaction4);

        when(namedParameterJdbcTemplate.query(anyString(), anyMap(), any(TransactionDetailsRowMapper.class)))
                .thenReturn(expectedResponse);

        EntityDataReadinessDetails result = entityDataReadinessDetailsDaoImpl.getEntityDetailsResponse(tenantId, request);

        assertNotNull(result);
        assertEquals(entityId, result.getEntityId());
        assertEquals(tenantId, result.getTenantId());
        assertEquals(3, result.getTotalTransactionsCount());
    }

    @Test
    public void testGetEntityDetailsResponseNoTransactions() {
        EntityDetailsRequestDTO request = new EntityDetailsRequestDTO();
        request.setStartDate(ZonedDateTime.parse("2024-01-01T05:00:00Z"));
        request.setEndDate(ZonedDateTime.parse("2024-01-31T05:00:00Z"));
        String tenantId = "testTenantId";
        String entityId = "testEntityId";
        request.setEntityId(entityId);

        List<EntityDataReadinessDetailsDTO> expectedResponse = new ArrayList<>();
		when(namedParameterJdbcTemplate.query(anyString(), anyMap(), any(TransactionDetailsRowMapper.class)))
				.thenReturn(expectedResponse);

        EntityDataReadinessDetails result = entityDataReadinessDetailsDaoImpl.getEntityDetailsResponse(tenantId, request);

        assertNotNull(result);
        assertEquals(entityId, result.getEntityId());
        assertEquals(tenantId, result.getTenantId());
        assertEquals(0, result.getTotalLinesCount());
        assertEquals(0, result.getTotalTransactionsCount());
        assertEquals(0, result.getErrorLinesCount());

    }

    @Test
    public void testQuantityQualityMetrics() {
        String tenantId = "tenantId1", transactionIdCode1 = "TID1", transactionIdCode2 = "TID2",
                transactionIdCode3 = "TID3", postingDate = "2024-01-01", entityId = "testEntityId";
        List<EntityDataReadinessDetailsDTO> transactions = Arrays.asList(
                new EntityDataReadinessDetailsDTO(tenantId, transactionIdCode1, "TID1-LID1", "LN1", postingDate, 1, "Processed successfully"),
                new EntityDataReadinessDetailsDTO(tenantId, transactionIdCode1, "TID1-LID2", "LN2", postingDate, 11, "Processed successfully with warning"),
                new EntityDataReadinessDetailsDTO(tenantId, transactionIdCode1, "TID1-LID3", "LN3", postingDate, 19, "Processed successfully with warning"),
                new EntityDataReadinessDetailsDTO(tenantId, transactionIdCode2, "TID2-LID1", "LN1", postingDate, 1, "Processed successfully"),
                new EntityDataReadinessDetailsDTO(tenantId, transactionIdCode2, "TID2-LID2", "LN2", postingDate, 0, "Failed"),
                new EntityDataReadinessDetailsDTO(tenantId, transactionIdCode2, "TID2-LID3", "LN3", postingDate, 13, "Failed"),
                new EntityDataReadinessDetailsDTO(tenantId, transactionIdCode3, "TID3-LID1", "LN1", postingDate, 2, "Processed with warning"),
                new EntityDataReadinessDetailsDTO(tenantId, transactionIdCode3, "TID3-LID2", "LN2", postingDate, 1, "Processed successfully"),
                new EntityDataReadinessDetailsDTO(tenantId, null, "NULL-LID1", "LN1", postingDate, 1, null)
        );
        EntityDetailsRequestDTO request = new EntityDetailsRequestDTO ();
        request.setStartDate(ZonedDateTime.parse("2024-01-01T05:00:00Z"));
        request.setEndDate(ZonedDateTime.parse("2024-01-31T05:00:00Z"));
        request.setEntityId(entityId);

        Map<String, Object> params = new HashMap<>();
        params.put("tenantId", tenantId);
        params.put("entityId", entityId);
        params.put("startDate", "2024-01-01");
        params.put("endDate", "2024-01-31");

        when(namedParameterJdbcTemplate.query(anyString(), anyMap(), any(TransactionDetailsRowMapper.class)))
                .thenReturn(transactions);

		EntityDataReadinessDetails result = entityDataReadinessDetailsDaoImpl.getEntityDetailsResponse(tenantId, request);

        assertNotNull(result);
        assertEquals(4, result.getTotalTransactionsCount());
        assertEquals(9, result.getTotalLinesCount());
        assertEquals(2, result.getSuccessfulTransactionsCount());
        assertEquals(7, result.getSuccessfulLinesCount());
        assertEquals(1, result.getErrorLinesCount());
    }


}

```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/datareadiness/mapper/TransactionDetailsRowMapperTest.java`

```java
package com.vertex.cnc.itc.datareadiness.mapper;

import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessDetailsDTO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.sql.ResultSet;
import java.sql.SQLException;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class TransactionDetailsRowMapperTest {

    private TransactionDetailsRowMapper rowMapper;
    private ResultSet resultSet;

    @BeforeEach
    void setUp() {
        rowMapper = new TransactionDetailsRowMapper();
        resultSet = mock(ResultSet.class);
    }

    @Test
    void ShouldMapResultSetToEntityDataDetailsDTO() throws SQLException {
        when(resultSet.getString("TENANT_ID")).thenReturn("123");
        when(resultSet.getString("TRANSACTION_ID")).thenReturn("TX1001");
        when(resultSet.getString("LINE_ITEM_ID")).thenReturn("LI567");
        when(resultSet.getString("LINE_ITEM_NUMBER")).thenReturn("42");
        when(resultSet.getString("POSTING_DATE")).thenReturn("2024-03-25");
        when(resultSet.getInt("DF_IS_PROCESSED")).thenReturn(1);
        when(resultSet.getString("PROCESSING_MESSAGE")).thenReturn("Processed Successfully");

        EntityDataReadinessDetailsDTO result = rowMapper.mapRow(resultSet, 1);

        assertNotNull(result);
        assertEquals("123", result.getTenantId());
        assertEquals("TX1001", result.getTransactionIdCode());
        assertEquals("LI567", result.getLineItemIdCode());
        assertEquals("42", result.getLineItemNumber());
        assertEquals("2024-03-25", result.getPostingDate());
        assertEquals(1, result.getDfIsProcessed());
        assertEquals("Processed Successfully", result.getProcessingMessage());

    }

    @Test
    void ShouldHandleNullValues() throws SQLException {
        when(resultSet.getString("TENANT_ID")).thenReturn(null);
        when(resultSet.getString("TRANSACTION_ID")).thenReturn(null);
        when(resultSet.getString("LINE_ITEM_ID")).thenReturn(null);
        when(resultSet.getString("LINE_ITEM_NUMBER")).thenReturn(null);
        when(resultSet.getString("POSTING_DATE")).thenReturn(null);
        when(resultSet.getInt("DF_IS_PROCESSED")).thenReturn(0);
        when(resultSet.getString("PROCESSING_MESSAGE")).thenReturn(null);

        EntityDataReadinessDetailsDTO result = rowMapper.mapRow(resultSet, 1);

        assertNotNull(result);
        assertNull(result.getTenantId());
        assertNull(result.getTransactionIdCode());
        assertNull(result.getLineItemIdCode());
        assertNull(result.getLineItemNumber());
        assertNull(result.getPostingDate());
        assertEquals(0, result.getDfIsProcessed());
        assertNull(result.getProcessingMessage());
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/datareadiness/mapper/EntityDataReadinessSummaryResponseDTORowMapperTest.java`

```java
package com.vertex.cnc.itc.datareadiness.mapper;

import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessSummaryResponseDTO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class EntityDataReadinessSummaryResponseDTORowMapperTest {

    @Mock
    private ResultSet resultSet;

    private EntityDataReadinessSummaryDTORowMapper entityDataReadinessSummaryDTORowMapper;

    @BeforeEach
    public void setUp() {
        entityDataReadinessSummaryDTORowMapper = new EntityDataReadinessSummaryDTORowMapper();
    }

    @Test
    public void testMapRow() throws SQLException {
        when(resultSet.next()).thenReturn(false);
        when(resultSet.getString("ENTITY_ID")).thenReturn("entity123");
        when(resultSet.getString("ENTITY_NAME")).thenReturn("Test Entity");
        when(resultSet.getString("PARENT_ENTITY_ID")).thenReturn("parent123");
        when(resultSet.getString("DATA_READINESS_STATUS")).thenReturn("Not Ready");

        List<EntityDataReadinessSummaryResponseDTO> result = entityDataReadinessSummaryDTORowMapper.mapRow(resultSet, 1);

        assertNotNull(result);
        assertEquals(1, result.size());

        EntityDataReadinessSummaryResponseDTO entity = result.getFirst();
        assertEquals("entity123", entity.getEntityId());
        assertEquals("Test Entity", entity.getEntityName());
        assertEquals("parent123", entity.getParentEntityId());
        assertEquals("Not Ready", entity.getDataReadinessStatus());
    }


}
```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/datareadiness/controller/DataReadinessControllerC4Test.java`

```java
package com.vertex.cnc.itc.datareadiness.controller;
import com.vertex.cnc.itc.common.exception.ApiException;
import com.vertex.cnc.itc.common.exception.RecordNotFoundException;
import com.vertex.cnc.itc.datareadiness.controller.impl.DataReadinessControllerImpl;
import com.vertex.cnc.itc.datareadiness.dto.request.CompletenessRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityDetailsRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityRequestDTO;
import com.vertex.cnc.itc.datareadiness.enums.DataReadinessStatusEnum;
import com.vertex.cnc.itc.datareadiness.response.DataReadinessSummary;
import com.vertex.cnc.itc.datareadiness.response.EntityDataCompleteness;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessDetails;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessSummary;
import com.vertex.cnc.itc.datareadiness.service.DataReadinessService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class DataReadinessControllerC4Test {

    @Mock
    private DataReadinessService dataReadinessService;

    @InjectMocks
    private DataReadinessControllerImpl dataReadinessController;

    @Test
    void testGetTenantEntities() {
        EntityRequestDTO request = new EntityRequestDTO();
        // Set request parameters here

        DataReadinessSummary summary = new DataReadinessSummary();

        HashMap<String,Integer> counts =new HashMap<>();
        counts.put(DataReadinessStatusEnum.NOT_READY.getStatus(),0);
        counts.put(DataReadinessStatusEnum.NEEDS_REVIEW.getStatus(),0);
        counts.put(DataReadinessStatusEnum.VALIDATED_DATA.getStatus(),0);
        summary.setStatusCounts(counts);
        List<EntityDataReadinessSummary> entityDataReadinessSummaries = new ArrayList<>();
        EntityDataReadinessSummary entityDataReadinessSummary = new EntityDataReadinessSummary();
        entityDataReadinessSummary.setEntityName("Test Entity");
        entityDataReadinessSummary.setDataReadinessStatus(DataReadinessStatusEnum.VALIDATED_DATA.getStatus());
        entityDataReadinessSummary.setEntityId("12345");
        entityDataReadinessSummary.setParentEntityId(null);
        entityDataReadinessSummary.setChildren(null);
        entityDataReadinessSummaries.add(entityDataReadinessSummary);
        summary.setEntityDataReadinessSummaries(entityDataReadinessSummaries); // Set this to a valid list if needed

        given(dataReadinessService.getTenantEntities(request)).willReturn(summary);

        DataReadinessSummary result = dataReadinessController.getTenantEntities(request);
        assertNotNull(result);
        assertNotNull(result.getEntityDataReadinessSummaries());
        assertNotNull(result.getStatusCounts());
        assertEquals(1, result.getEntityDataReadinessSummaries().size());
    }

    @Test
    void testGetEntityDataReadinessDetails() {
        EntityDetailsRequestDTO request = new EntityDetailsRequestDTO();
        request.setStartDate(ZonedDateTime.now());
        request.setEndDate(ZonedDateTime.now().plusDays(1));
        request.setEntityId("12345");

        EntityDataReadinessDetails details = new EntityDataReadinessDetails();
        details.setEntityId("12345");
        details.setTenantId("abcdefa232");

        given(dataReadinessService.getEntityDetails(request)).willReturn(details);

        EntityDataReadinessDetails result = dataReadinessController.getEntityDataReadinessDetails(request);

        // Validate the response
        assertNotNull(result);
        assertEquals("12345", result.getEntityId());
        assertEquals("abcdefa232", result.getTenantId());
    }

    @Test
    void testGetEntityDataReadinessDetailsWhenNull() {
        given(dataReadinessService.getEntityDetails(null)).willReturn(null);

        EntityDataReadinessDetails result = dataReadinessController.getEntityDataReadinessDetails(null);
        assertNull(result);
    }

    @Test
    void testGetEntityDataReadiness_throwsException_asExpected() {
        EntityDetailsRequestDTO request = EntityDetailsRequestDTO.builder()
                .startDate(ZonedDateTime.now())
                .endDate(ZonedDateTime.now().plusDays(1))
                .entityId("12345-123-1122")
                .build();

        when(dataReadinessService.getEntityDetails(request)).thenThrow(RecordNotFoundException.class);

        assertThrows(ApiException.class, () ->
                dataReadinessController.getEntityDataReadinessDetails(request));
    }

    @Test
    void testGetTenantEntitiesWhenNull() {
        given(dataReadinessService.getTenantEntities(null)).willReturn(null);

        DataReadinessSummary result = dataReadinessController.getTenantEntities(null);
        assertNull(result);
    }

    @Test
    void testGetTenantEntitiesNotFound() {
        given(dataReadinessService.getTenantEntities(null)).willThrow(new RuntimeException("Not Found"));

        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            dataReadinessController.getTenantEntities(null);
        });
        String error = "Error occurred while fetching tenant entitiesjava.lang.RuntimeException: Not Found";
        assertEquals(error, exception.getMessage());
    }

    @Test
    void testGetEntityCompleteness_Works_asExpected() {

        EntityDataCompleteness expectedEntityDataCompleteness = EntityDataCompleteness.builder()
                .currentPeriodNumber(3)
                .previousPeriodNumber(2)
                .currentPeriodStartDate(LocalDate.now().minusDays(1))
                .currentPeriodEndDate(LocalDate.now())
                .build();

        CompletenessRequestDTO completenessRequest = CompletenessRequestDTO.builder()
                .entityId("12345-123-1122")
                .startDate(LocalDate.now())
                .endDate(LocalDate.now().plusDays(1))
                .build();

        when(dataReadinessService.getCompletenessEntityDetails(any(CompletenessRequestDTO.class)))
                .thenReturn(expectedEntityDataCompleteness);

        EntityDataCompleteness actualEntityDataCompleteness =
                dataReadinessController.getEntityCompleteness(completenessRequest);

        assertEquals(expectedEntityDataCompleteness, actualEntityDataCompleteness);
    }

    @Test
    void testGetEntityCompleteness_throwsException_asExpected() {

        CompletenessRequestDTO completenessRequest = CompletenessRequestDTO.builder()
                .entityId("12345-123-1122")
                .startDate(LocalDate.now())
                .endDate(LocalDate.now().plusDays(1))
                .build();

        when(dataReadinessService.getCompletenessEntityDetails(any(CompletenessRequestDTO.class)))
                .thenThrow(RecordNotFoundException.class);

        assertThrows(ApiException.class, () ->
                dataReadinessController.getEntityCompleteness(completenessRequest));

    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/datareadiness/controller/DataReadinessControllerC3Test.java`

```java
package com.vertex.cnc.itc.datareadiness.controller;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.vertex.cnc.itc.common.constants.ApplicationConstants;
import com.vertex.cnc.itc.common.exception.RecordNotFoundException;
import com.vertex.cnc.itc.datareadiness.dto.request.CompletenessRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityDetailsRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityRequestDTO;
import com.vertex.cnc.itc.datareadiness.response.DataReadinessSummary;
import com.vertex.cnc.itc.datareadiness.response.EntityDataCompleteness;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessDetails;
import com.vertex.cnc.itc.datareadiness.service.DataReadinessService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDate;
import java.time.ZonedDateTime;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;


@WebMvcTest(DataReadinessController.class)
@AutoConfigureMockMvc(addFilters = false)
@ActiveProfiles(ApplicationConstants.TEST_PROFILE)
public class DataReadinessControllerC3Test {

    @MockitoBean
    private DataReadinessService dataReadinessService;

    @Autowired
    private DataReadinessController dataReadinessController;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private MockMvc mockMvc;

    @Test
    void testGetTenantEntities() throws Exception {
        EntityRequestDTO request = new EntityRequestDTO();
        // Set request parameters here

        DataReadinessSummary summary = new DataReadinessSummary();
        // Set summary data here

        when(dataReadinessService.getTenantEntities(request)).thenReturn(summary);

        mockMvc.perform(post("/v1/data-readiness/entities")
                        .contentType("application/json")
                        .content("{ \"startDate\": \"2025-03-19T14:38:24.524Z\", " +
                                "\"endDate\": \"2025-03-29T14:38:24.524Z\", \"periodId\": \"bruh\" }"))
                .andExpect(status().isOk());
    }

    @Test
    void testGetEntityDataReadinessDetails() throws Exception {
        EntityDetailsRequestDTO request = new EntityDetailsRequestDTO();
        request.setStartDate(ZonedDateTime.now());
        request.setEndDate(ZonedDateTime.now().plusDays(1));
        request.setEntityId("12345");

        EntityDataReadinessDetails details = new EntityDataReadinessDetails();
        details.setEntityId("12345");
        details.setTenantId("abcdefa232");

        when(dataReadinessService.getEntityDetails(any(EntityDetailsRequestDTO.class))).thenReturn(details);

        // Validate response
         mockMvc.perform(post("/v1/data-readiness/entity")
                        .contentType("application/json")
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk());

    }

    @Test
    void testGetEntityDataReadinessDetailsValidationFails() throws Exception {
        EntityDetailsRequestDTO request = new EntityDetailsRequestDTO();

        mockMvc.perform(post("/v1/data-readiness/entity")
                        .contentType("application/json")
                        .content(request.toString()))
                .andExpect(status().isBadRequest());
    }

    @Test
    void testGetTenantEntitiesBadRequest() throws Exception {
        when(dataReadinessService.getTenantEntities(any(EntityRequestDTO.class))).thenThrow(new RuntimeException("Not Found"));

        mockMvc.perform(post("/v1/data-readiness/entities")
                        .contentType("application/json")
                        .content("{ \"startDate\": \"2\", " +
                                "\"endDate\": \"4Z\", \"periodId\": \"periodId\" }"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void testGetEntityCompleteness_works_AsExpected() throws Exception {
        EntityDataCompleteness entityDataCompletenessResponse = EntityDataCompleteness.builder()
                .currentPeriodNumber(3)
                .previousPeriodNumber(2)
                .currentPeriodStartDate(LocalDate.now().minusDays(1))
                .currentPeriodEndDate(LocalDate.now())
                .build();

        when(dataReadinessService.getCompletenessEntityDetails(any(CompletenessRequestDTO.class)))
                .thenReturn(entityDataCompletenessResponse);

        CompletenessRequestDTO request =  CompletenessRequestDTO.builder()
                .entityId("12345-123-1122")
                .startDate(LocalDate.now())
                .endDate(LocalDate.now().plusDays(1))
                .build();

        this.mockMvc.perform(post("/v1/data-readiness/completeness")
                        .contentType("application/json")
                        .content(objectMapper.writeValueAsString(request)))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.currentPeriodNumber").value("3"))
                .andExpect(jsonPath("$.previousPeriodNumber").value("2"));
    }

    @Test
    void testGetEntityCompleteness_works_AsExpected_WithInvalidRequest() throws Exception {
        EntityDataCompleteness entityDataCompletenessResponse = EntityDataCompleteness.builder()
                .currentPeriodNumber(3)
                .previousPeriodNumber(2)
                .currentPeriodStartDate(LocalDate.now().minusDays(1))
                .currentPeriodEndDate(LocalDate.now())
                .build();

        when(dataReadinessService.getCompletenessEntityDetails(any(CompletenessRequestDTO.class)))
                .thenReturn(entityDataCompletenessResponse);

        CompletenessRequestDTO request =  CompletenessRequestDTO.builder()
                .build();

        this.mockMvc.perform(post("/v1/data-readiness/completeness")
                        .contentType("application/json")
                        .content(objectMapper.writeValueAsString(request)))
                .andDo(print())
                .andExpect(status().isBadRequest());
    }

    @Test
    void testGetEntityCompleteness_works_AsExpected_when_InternalExceptionOccurs() throws Exception {

        when(dataReadinessService.getCompletenessEntityDetails(any(CompletenessRequestDTO.class)))
                .thenThrow(RecordNotFoundException.class);

        CompletenessRequestDTO request =  CompletenessRequestDTO.builder()
                .entityId("12345-123-1122")
                .startDate(LocalDate.now())
                .endDate(LocalDate.now().plusDays(1))
                .build();

        this.mockMvc.perform(post("/v1/data-readiness/completeness")
                        .contentType("application/json")
                        .content(objectMapper.writeValueAsString(request)))
                .andDo(print())
                .andExpect(status().isInternalServerError());
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/datareadiness/controller/DataReadinessControllerC2Test.java`

```java
package com.vertex.cnc.itc.datareadiness.controller;

import com.vertex.cnc.itc.configuration.SecurityTestConfig;
import com.vertex.cnc.itc.configuration.TestApplicationFilter;
import com.vertex.cnc.itc.datareadiness.dto.request.CompletenessRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityDetailsRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityRequestDTO;
import com.vertex.cnc.itc.datareadiness.response.DataReadinessSummary;
import com.vertex.cnc.itc.datareadiness.response.EntityDataCompleteness;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessDetails;
import com.vertex.cnc.itc.security.dto.Role;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.context.annotation.Import;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.RequestEntity;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.ContextConfiguration;

import java.net.URI;
import java.time.LocalDate;
import java.time.ZonedDateTime;

import static com.vertex.cnc.itc.common.constants.ApplicationConstants.TEST_PROFILE;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles(TEST_PROFILE)
@Import({ SecurityTestConfig.class, TestApplicationFilter.class })
@ContextConfiguration(classes = { SecurityTestConfig.class })
public class DataReadinessControllerC2Test {

    @Autowired
    private TestRestTemplate restTemplate;

    @BeforeEach
    public void setup() {
        Role role = new Role().builder()
                .platformProductCode("tta-ind-tax-close")
                .userRoleCode("tta-itc-data-admin")
                .userRoleName("Data Admin")
                .build();
        TestApplicationFilter.setTestRole(role);

    }

    @Test
    void testGetTenantEntities() {
        EntityRequestDTO request = new EntityRequestDTO();
        // Set request parameters here
        ZonedDateTime startDate = ZonedDateTime.now().minusDays(5);
        ZonedDateTime endDate = ZonedDateTime.now();
        request.setStartDate(startDate);
        request.setEndDate(endDate);
        request.setPeriodId("bruh");
        RequestEntity<EntityRequestDTO> req = new RequestEntity<>(request, HttpMethod.POST, URI.create("/v1/data-readiness/entities"));

        ResponseEntity<DataReadinessSummary> response = restTemplate.exchange(
                "/v1/data-readiness/entities",
                HttpMethod.POST,
                req,
                new ParameterizedTypeReference<DataReadinessSummary>() {
                });

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
    }

    @Test
    void testGetEntityDataReadinessDetails() {
        EntityDetailsRequestDTO request = new EntityDetailsRequestDTO();
        // Set request parameters here
        ZonedDateTime startDate = ZonedDateTime.now().minusDays(5);
        ZonedDateTime endDate = ZonedDateTime.now();
        request.setStartDate(startDate);
        request.setEndDate(endDate);
        request.setEntityId("123");
        RequestEntity<EntityDetailsRequestDTO> req = new RequestEntity<>(request, HttpMethod.POST, URI.create("/v1/data-readiness/entity"));

        ResponseEntity<EntityDataReadinessDetails> response = restTemplate.exchange(
                "/v1/data-readiness/entity",
                HttpMethod.POST,
                req,
                new ParameterizedTypeReference<EntityDataReadinessDetails>() {
                });

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
    }

    @Test
    void testGetTenantEntitiesWhenUrlIsIncorrect() {
        ResponseEntity<Object> response = restTemplate.exchange(
                "/v1/data-readiness/incorrect-url",
                HttpMethod.POST,
                null,
                Object.class);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void testGetEntityCompletenessDetails() {
        CompletenessRequestDTO request = CompletenessRequestDTO.builder()
                .startDate(LocalDate.parse("2024-12-01"))
                .endDate(LocalDate.parse("2024-12-31"))
                .entityId("entityId")
                .build();

        RequestEntity<CompletenessRequestDTO> req = new RequestEntity<>(request, HttpMethod.POST, URI.create("/v1/data-readiness/completeness"));

        ResponseEntity<EntityDataCompleteness> response = restTemplate.exchange(
                "/v1/data-readiness/completeness",
                HttpMethod.POST,
                req,
                new ParameterizedTypeReference<EntityDataCompleteness>() {
                });

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
    }
}
```

## 📄 `../vertexinc/cnc-itc-api/src/test/java/com/vertex/cnc/itc/datareadiness/service/DataReadinessServiceTest.java`

```java
package com.vertex.cnc.itc.datareadiness.service;

import com.vertex.cnc.itc.datareadiness.dao.impl.EntityDaoImpl;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityRequestDTO;
import com.vertex.cnc.itc.datareadiness.response.DataReadinessSummary;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityDetailsRequestDTO;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessDetails;
import com.vertex.cnc.itc.datareadiness.service.impl.DataReadinessServiceImpl;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.mockito.Mockito.verify;

@ExtendWith(MockitoExtension.class)
public class DataReadinessServiceTest {

    @Mock
    private DataReadinessServiceImpl dataReadinessService;

    @Mock
    private EntityDaoImpl entityDao;

    @InjectMocks
    private DataReadinessServiceImpl dailyJobService;

    @Test
    public void testGetTenantEntities() {
        DataReadinessSummary expected = new DataReadinessSummary();
        Mockito.when(dataReadinessService.getTenantEntities(Mockito.any(EntityRequestDTO.class)))
                .thenReturn(new DataReadinessSummary());
        DataReadinessSummary result = dataReadinessService.getTenantEntities(new EntityRequestDTO());

        Assertions.assertNotNull(result);
        Assertions.assertEquals(result, expected);
    }

    @Test
    public void testGetEntityDetails(){
        EntityDataReadinessDetails expected = new EntityDataReadinessDetails();
        Mockito.when(dataReadinessService.getEntityDetails(Mockito.any(EntityDetailsRequestDTO.class)))
                .thenReturn(new EntityDataReadinessDetails());
        EntityDataReadinessDetails result = dataReadinessService.getEntityDetails(new EntityDetailsRequestDTO());

        Assertions.assertNotNull(result);
        Assertions.assertEquals(result, expected);
    }

    @Test
    public void testLoadClientEntityPeriodItcStatus() {
        dailyJobService.loadClientEntityPeriodItcStatus();
        verify(entityDao).loadClientEntityPeriodItcStatus();
    }

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/CncItcApiApplication.java`

```java
package com.vertex.cnc.itc;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class CncItcApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(CncItcApiApplication.class, args);
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/ApiVersions.java`

```java
package com.vertex.cnc.itc.common;

public class ApiVersions {

	public static final String V1 = "/v1";

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/RequestMappings.java`

```java
package com.vertex.cnc.itc.common;

public class RequestMappings {

	public static final String HEALTH = "/health";

	public static final String ACTUATOR = "/actuator";

	public static final String SPRING_DOCS_SWAGGER = "/swagger-ui";

	public static final String SPRING_DOCS_OPENAPI = "/api-docs";

	public static final String PERIOD = "/period";

	public static final String ENTITIES = "/entities";

	public static final String ENTITY = "/entity";


	public static final String COMPLETENESS = "/completeness";

	public static final String DATA_READINESS = "/data-readiness";

	public static final String STATUS = "/status";


	public static final String PERMISSIONS = "/permissions";

	public static final String DATA_REVIEW = "/review";


	public static final String REPORTS = "/reports";
	public static final String REPORTVIEWS = "/dataviews";
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/aop/CNCITCContext.java`

```java
package com.vertex.cnc.itc.common.aop;

import com.vertex.cnc.itc.security.dto.Feature;
import com.vertex.cnc.itc.security.dto.Role;
import com.vertex.cnc.itc.security.dto.TenantProfile;
import com.vertex.cnc.itc.security.dto.UserProfile;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.slf4j.MDC;
import org.springframework.context.ApplicationContext;

import java.util.ArrayList;
import java.util.List;

/**
 * CNC Context class that must be set for all requests.
 */
@Data
@NoArgsConstructor
public class CNCITCContext {

	private static final Logger LOGGER = LogManager.getLogger(CNCITCContext.class);

	private static ThreadLocal<CNCITCContext> context = new InheritableThreadLocal<>() {

		/**
		 * Method invoked when inherited thread local is initialized for a new thread.
		 * Without this deep copy, a parent and child thread will share the same instance
		 * of the query context, resulting in data corruption.
		 * @param parent Parent query context from which child context to be initialized.
		 * @return New cloned child query context.
		 */
		@Override
		protected CNCITCContext childValue(CNCITCContext parent) {
			if (parent != null) {
				LOGGER.info("CNCConfigContext --> UserProfile - {}", parent.getUserProfile());
			}
			else {
				LOGGER.debug("CNCConfigContext --> parent is null");
			}
			return (parent != null) ? new CNCITCContext(parent) : null;
		}
	};

	private ApplicationContext applicationContext;

	private String token;

	private UserProfile userProfile;

	private List<Feature> features = new ArrayList<>();

	private Role role;

	private String clientName;

	private TenantProfile tenantProfile;

	/**
	 * Constructor to clone another CNCConfigContext instance.
	 */
	public CNCITCContext(CNCITCContext CNCITCContext) {
		this.applicationContext = CNCITCContext.getApplicationContext();
		this.token = CNCITCContext.getToken();
		this.userProfile = CNCITCContext.getUserProfile();
		this.features = CNCITCContext.getFeatures();
		this.role = CNCITCContext.getRole();
		this.clientName = CNCITCContext.getClientName();
		this.tenantProfile = CNCITCContext.getTenantProfile();
	}

	/**
	 * Gets the current CNC context from the thread-local storage. If no context exists, a
	 * new one is created and set for the thread.
	 */
	public static CNCITCContext getContext() {
		CNCITCContext context = CNCITCContext.context.get();
		if (context == null) {
			context = new CNCITCContext();
		}
		resetContext(context);
		return context;
	}

	public void buildTenantProfile(TenantProfile tenantProfile) {
		this.tenantProfile = tenantProfile;
		MDC.put("tenantID",this.tenantProfile.getTenantId());
	}

	public void setRole(Role role) {
		this.role = role;
		MDC.put("role",String.valueOf(this.role));
	}

	/**
	 * Sets the provided CNCConfigContext in the thread-local variable.
	 * @param context The CNCConfigContext to set.
	 */
	public static void resetContext(CNCITCContext context) {
		CNCITCContext.context.set(context);
	}

	/**
	 * Removes the CNCConfigContext from the thread-local storage.
	 */
	public static void resetContext() {
		CNCITCContext.context.remove();
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/utility/SnowFlakeDialect.java`

```java
package com.vertex.cnc.itc.common.utility;

import org.hibernate.dialect.DatabaseVersion;
import org.hibernate.dialect.sequence.SequenceSupport;
import org.springframework.context.annotation.Configuration;

import static com.vertex.cnc.itc.common.constants.DBConstants.MINIMUM_VERSION;

@Configuration
public class SnowFlakeDialect extends org.hibernate.dialect.Dialect {

	public SnowFlakeDialect() {
		this(MINIMUM_VERSION);
	}

	public SnowFlakeDialect(DatabaseVersion version) {
		super(version);
	}

	@Override
	protected DatabaseVersion getMinimumSupportedVersion() {
		return MINIMUM_VERSION;
	}

	@Override
	public SequenceSupport getSequenceSupport() {
		return new SnowFlakeSequenceSupport();
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/utility/SnowFlakeSequenceSupport.java`

```java
package com.vertex.cnc.itc.common.utility;

import org.hibernate.dialect.sequence.SequenceSupport;

public class SnowFlakeSequenceSupport implements SequenceSupport {

	@Override
	public String getSelectSequenceNextValString(String sequenceName) {
		return sequenceName + ".nextVal";
	}

	@Override
	public String getSequenceNextValString(String sequenceName) {
		return "select " + getSelectSequenceNextValString(sequenceName);
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/utility/WebClientUtils.java`

```java
package com.vertex.cnc.itc.common.utility;

import com.vertex.cnc.itc.common.exception.ApiException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.Collections;

public class WebClientUtils {
    private static final Logger logger = LogManager.getLogger(WebClientUtils.class);

    private final RestTemplate restTemplate;

    public WebClientUtils(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public <T> T performRestGet(String token, String uri, ParameterizedTypeReference<T> responseClass) throws RestClientException {
        ResponseEntity<T> responseEntity;

        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
        httpHeaders.add(HttpHeaders.AUTHORIZATION, token);
        HttpEntity<T> httpEntity = new HttpEntity<>(null, httpHeaders);

        responseEntity = restTemplate.exchange(uri, HttpMethod.GET, httpEntity, responseClass);
        logger.debug("Received a response from GET request: {}", responseEntity);

        if (responseEntity.getBody() == null) {
            logger.error("No response received from GET request for {}", uri);
            throw new ApiException("Did not get a body in the response.");
        }
        return responseEntity.getBody();
    }
}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/constants/DBConstants.java`

```java
package com.vertex.cnc.itc.common.constants;

import org.hibernate.dialect.DatabaseVersion;

public class DBConstants {

	public static final DatabaseVersion MINIMUM_VERSION = DatabaseVersion.make(7, 17);

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/constants/ApplicationConstants.java`

```java
package com.vertex.cnc.itc.common.constants;

public class ApplicationConstants {

	public static final String NOT_TEST_PROFILE = "!test";

	public static final String TEST_PROFILE = "test";

	public static final String RECORD_NOT_FOUND_CODE = "RECORD_NOT_FOUND";

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/exception/Errors.java`

```java
package com.vertex.cnc.itc.common.exception;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@JsonInclude(content = JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
@Data
public class Errors {

	private List<ApiErrorResponse> error = new ArrayList<>();

	@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "MM-dd-yyyy hh:mm:ss")
	private LocalDateTime timestamp;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/exception/ApiException.java`

```java
package com.vertex.cnc.itc.common.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

public class ApiException extends RuntimeException {

	@Getter
	private final String code;

	private final String message;

	@Getter
	private final HttpStatus status;

	public ApiException(HttpStatus status, String message, Exception exception) {
		super(exception);
		this.status = status;
		this.code = status.toString();
		this.message = message;
	}

	public ApiException(HttpStatus status, String message) {
		super();
		this.status = status;
		this.code = status.toString();
		this.message = message;
	}

	public ApiException(String message) {
		this(HttpStatus.INTERNAL_SERVER_ERROR, message);
	}

	@Override
	public String getMessage() {
		return message;
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/exception/UnauthorizedAccessException.java`

```java
package com.vertex.cnc.itc.common.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
public class UnauthorizedAccessException extends RuntimeException {

	private final HttpStatus status;

	private final String message;

	public UnauthorizedAccessException(String message) {
		super(message);
		this.status = HttpStatus.UNAUTHORIZED;
		this.message = message;
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/exception/ApiErrorResponse.java`

```java
package com.vertex.cnc.itc.common.exception;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;
import org.springframework.http.HttpStatus;

/**
 * Api error response DTO
 */
@JsonInclude(content = JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
@Data
@Getter
@Setter
public class ApiErrorResponse {

	private String code;

	private String message;

	private String source;

	private HttpStatus httpStatus;

	private int statusCode;

	public ApiErrorResponse(HttpStatus status, String message) {
		this.httpStatus = status;
		this.code = status.name();
		this.statusCode = status.value();
		this.message = message;
	}

	public ApiErrorResponse(String message) {
		this.message = message;
	}

	public ApiErrorResponse(HttpStatus status, String message, String code) {
		this(status, message);
		this.code = code;
	}

	public ApiErrorResponse(String code, String message, String source) {
		this.code = code;
		this.message = message;
		this.source = source;
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/common/exception/RecordNotFoundException.java`

```java
package com.vertex.cnc.itc.common.exception;

import org.springframework.http.HttpStatus;

public class RecordNotFoundException extends ApiException{
    private final String code;

    /**
     * Constructor for RecordNotFoundException
     * @param code - error code
     * @param message - error message
     */
    public RecordNotFoundException(String code, String message) {
        super(HttpStatus.NOT_FOUND, message);
        this.code = code;
    }

    @Override
    public String getCode() { return code; }

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/CNCITCAuthTokenToUserProfileFilter.java`

```java
package com.vertex.cnc.itc.security;

import com.vertex.cnc.itc.common.RequestMappings;
import com.vertex.cnc.itc.common.aop.CNCITCContext;
import com.vertex.cnc.itc.common.exception.UnauthorizedAccessException;
import com.vertex.cnc.itc.security.dto.TenantProfile;
import com.vertex.cnc.itc.security.dto.UserProfile;
import com.vertex.cnc.itc.security.service.VertexCloudService;
import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.text.ParseException;
import java.util.Arrays;

import static com.vertex.cnc.itc.common.constants.ApplicationConstants.NOT_TEST_PROFILE;

@Component
@Profile(NOT_TEST_PROFILE)
public class CNCITCAuthTokenToUserProfileFilter implements Filter {

	private static final String[] UNSECURED_SPRING_PATHS = new String[] { RequestMappings.SPRING_DOCS_SWAGGER,
			RequestMappings.SPRING_DOCS_OPENAPI, RequestMappings.ACTUATOR };

	private static final String[] UNSECURED_ENDPOINTS = new String[] { RequestMappings.HEALTH };

	private static final Logger logger = LogManager.getLogger(CNCITCAuthTokenToUserProfileFilter.class);

	private final VertexCloudService vertexCloudService;

	private final ApplicationContext applicationContext;

	@Autowired
	public CNCITCAuthTokenToUserProfileFilter(VertexCloudService vertexCloudService,
											  ApplicationContext applicationContext) {
		this.vertexCloudService = vertexCloudService;
		this.applicationContext = applicationContext;
	}

	@Override
	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
			throws IOException, ServletException {

		HttpServletRequest httpServletRequest = (HttpServletRequest) request;
		HttpServletResponse httpServletResponse = (HttpServletResponse) response;

		String token = httpServletRequest.getHeader("Authorization");
		if (!shouldSkipFilter(request)) {
			if (token == null || token.isEmpty()) {
				logger.warn("Authorization token is missing");
				throw new UnauthorizedAccessException("Authorization token is missing");
			}

			// Fetch the user profile and tenant profile using the token from
			// VertexCloudService
			try {
				UserProfile userProfile = vertexCloudService.fetchUserProfile(token);
				TenantProfile tenantProfile = vertexCloudService.fetchTenantProfile(token);

				if (userProfile == null || tenantProfile == null) {
					throw new UnauthorizedAccessException("Invalid token or profiles not found.");
				}

				logger.debug("User profile fetched successfully {}", tenantProfile);
				CNCITCContext.getContext().setApplicationContext(applicationContext);
				CNCITCContext.getContext().setToken(token);
				CNCITCContext.getContext().setUserProfile(userProfile);
				CNCITCContext.getContext().buildTenantProfile(tenantProfile);

			}
			catch (ParseException e) {
				throw new RuntimeException(e);
			}

		}

		chain.doFilter(request, response);
	}

	/**
	 * Determines whether an auth filter should be skipped. This should return true for
	 * requests that do not need to be authenticated (i.e., to get a config value back to
	 * the UI).
	 * @param request the request
	 * @return true if filter should be skipped, false otherwise and by default
	 */
	protected boolean shouldSkipFilter(ServletRequest request) {
		boolean skipFilter = false;

		if (request instanceof HttpServletRequest) {
			String url = ((HttpServletRequest) request).getRequestURL().toString();
			skipFilter = isUnsecuredEndpoint(url);
		}

		return skipFilter;
	}

	private boolean isUnsecuredEndpoint(String url) {
		return Arrays.stream(UNSECURED_ENDPOINTS).anyMatch(url::endsWith)
				|| Arrays.stream(UNSECURED_SPRING_PATHS).anyMatch(url::contains);
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/configuration/CustomPermissionEvaluator.java`

```java
package com.vertex.cnc.itc.security.configuration;

import com.vertex.cnc.itc.security.service.UserPermissionService;
import org.springframework.security.access.PermissionEvaluator;
import org.springframework.security.core.Authentication;

import java.io.Serializable;

public class CustomPermissionEvaluator implements PermissionEvaluator {

    private final UserPermissionService userPermissionService;

    public CustomPermissionEvaluator(UserPermissionService userPermissionService) {
        this.userPermissionService = userPermissionService;
    }

    @Override
    public boolean hasPermission(Authentication authentication, Object targetDomainObject, Object permission) {
        if (targetDomainObject instanceof String && permission instanceof String) {
            return userPermissionService.hasPermission((String) targetDomainObject, (String) permission);
        }
        return false;
    }

    @Override
    public boolean hasPermission(Authentication authentication, Serializable targetId, String targetType, Object permission) {
        if (targetId == null || targetType == null || permission == null) {
            return false;
        }
    
        if (!(permission instanceof String)) {
            return false;
        }
    
        // Delegate the permission check to the UserPermissionService
        return userPermissionService.hasPermissionByIdAndType(authentication.getName(), targetId, targetType, (String) permission);
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/configuration/OAuth2ResourceServerSecurityConfiguration.java`

```java
package com.vertex.cnc.itc.security.configuration;

import com.vertex.cnc.itc.common.RequestMappings;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.oauth2.server.resource.authentication.JwtIssuerAuthenticationManagerResolver;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.csrf.CookieCsrfTokenRepository;

import static com.vertex.cnc.itc.common.constants.ApplicationConstants.NOT_TEST_PROFILE;

@Configuration
@EnableWebSecurity
@NoArgsConstructor
@Profile(NOT_TEST_PROFILE)
public class OAuth2ResourceServerSecurityConfiguration {

	@Value("${spring.security.oauth2.resourceserver.jwt.issuer-vertex}")
	private String vertexIssuer;

	@Value("${spring.security.oauth2.resourceserver.jwt.issuer-auth0}")
	private String auth0Issuer;

	@Value("${spring.security.oauth2.resourceserver.cnc-scope}")
	private String cncScopeSecurity;

	@Bean
	protected SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
		String cncScope = "SCOPE_" + this.cncScopeSecurity;
		JwtIssuerAuthenticationManagerResolver authenticationManagerResolver = JwtIssuerAuthenticationManagerResolver
			.fromTrustedIssuers(vertexIssuer, auth0Issuer);
		configureCorsAndCsrf(http);
		configurePermitAll(http);
		configureAuthority(http, cncScope);
		http.oauth2ResourceServer(oauth2 -> oauth2.authenticationManagerResolver(authenticationManagerResolver));
		return http.build();
	}

	private void configureCorsAndCsrf(HttpSecurity http) throws Exception {
		http.cors(Customizer.withDefaults())
			.csrf(csrf -> csrf.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()));
	}

	private void configurePermitAll(HttpSecurity http) throws Exception {
		http.authorizeHttpRequests(authorize -> authorize.requestMatchers(RequestMappings.ACTUATOR + "/health")
			.permitAll()
			// ... (all the other permitAll() rules from the original code)
			.requestMatchers(RequestMappings.SPRING_DOCS_SWAGGER + "/**")
			.permitAll()
			.requestMatchers("/api-docs/**", "/swagger-resources/**", "/webjars/**")
			.permitAll()
			.requestMatchers(RequestMappings.SPRING_DOCS_SWAGGER + "*")
			.permitAll()
			.requestMatchers(RequestMappings.SPRING_DOCS_OPENAPI + "/**")
			.permitAll()
			.requestMatchers(RequestMappings.SPRING_DOCS_OPENAPI + "*")
			.permitAll()
			.requestMatchers(HttpMethod.OPTIONS, "/**")
			.permitAll());
	}

	private void configureAuthority(HttpSecurity http, String cncScope) throws Exception {
		http.authorizeHttpRequests(authorize -> authorize.requestMatchers(HttpMethod.GET, "/**")
			.hasAuthority(cncScope)
			.requestMatchers(HttpMethod.POST, "/**")
			.hasAuthority(cncScope)
			.requestMatchers(HttpMethod.DELETE, "/**")
			.hasAuthority(cncScope)
			.requestMatchers(HttpMethod.PATCH, "/**")
			.hasAuthority(cncScope)
			// ... (all the other hasAuthority() rules from the original code)
			.anyRequest()
			.authenticated());
	}

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/configuration/AppConfig.java`

```java
package com.vertex.cnc.itc.security.configuration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class AppConfig {

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/dto/Subscription.java`

```java
package com.vertex.cnc.itc.security.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Subscription {

	private String id;

	private String status;

	private List<Feature> features;

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/dto/UserAccessPermissionResponseDTO.java`

```java
package com.vertex.cnc.itc.security.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserAccessPermissionResponseDTO {

	private String dataTestId;

	private String permissionLevel;

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/dto/Feature.java`

```java
package com.vertex.cnc.itc.security.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Feature {

	private String platformProductCode;

	private String featureCode;

	private String featureName;

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/dto/UserProfile.java`

```java
package com.vertex.cnc.itc.security.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserProfile {

	private String sub;

	private String first_name;

	private String preferred_username;

	private String impersonation_vtms_user_id;

	private String family_name;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/dto/Role.java`

```java
package com.vertex.cnc.itc.security.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Role {

	private String platformProductCode;

	private String userRoleCode;

	private String userRoleName;

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/dto/TenantProfile.java`

```java
package com.vertex.cnc.itc.security.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TenantProfile {

	private String tenantId;

	private List<Role> roles;

	private Subscription subscription;

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/controller/PermissionController.java`

```java
package com.vertex.cnc.itc.security.controller;

import com.vertex.cnc.itc.common.ApiVersions;
import com.vertex.cnc.itc.common.RequestMappings;
import com.vertex.cnc.itc.security.dto.UserAccessPermissionResponseDTO;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Tag(name = "Permissions", description = """
		<b>Description</b><br />
		<p>
		    This API provides the list of features with permissions.
		</p>

		<b>Additional Links</b><br />
		<ul>
		    <li>
		        <a href= target='_blank'>
		        Permissions Brief</a>
		    </li>
		</ul>

		""")
@Validated
@RequestMapping(value = ApiVersions.V1 + RequestMappings.PERMISSIONS)
public interface PermissionController {
    @GetMapping
	List<UserAccessPermissionResponseDTO> getUserAccessPermissions();
}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/controller/impl/PermissionControllerImpl.java`

```java
package com.vertex.cnc.itc.security.controller.impl;

import com.vertex.cnc.itc.security.controller.PermissionController;
import com.vertex.cnc.itc.security.dto.UserAccessPermissionResponseDTO;
import com.vertex.cnc.itc.security.service.PermissionService;
import lombok.AllArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
@AllArgsConstructor
@RestController
public class PermissionControllerImpl implements PermissionController {

    private final PermissionService permissionService;
    private static final Logger logger = LogManager.getLogger(PermissionControllerImpl.class);


    @Override
    public List<UserAccessPermissionResponseDTO> getUserAccessPermissions() {
        
        if(permissionService == null){
            logger.error("Invalid PermissionService state. PermissionService is null");
            return null;
        }
        return permissionService.getUserAccessPermissions();
    }
}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/service/UserPermissionService.java`

```java
package com.vertex.cnc.itc.security.service;

import java.io.Serializable;

public interface UserPermissionService {

    boolean hasPermission(String dataTestId, String permissionLevel);
    public boolean hasPermissionByIdAndType(String username, Serializable targetId, String targetType, String permission);

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/service/PermissionService.java`

```java
package com.vertex.cnc.itc.security.service;

import com.vertex.cnc.itc.security.dto.UserAccessPermissionResponseDTO;
import org.springframework.http.ResponseEntity;

import java.util.List;

public interface PermissionService {
    List<UserAccessPermissionResponseDTO> getUserAccessPermissions();
}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/service/VertexCloudService.java`

```java
package com.vertex.cnc.itc.security.service;

import com.vertex.cnc.itc.security.dto.TenantProfile;
import com.vertex.cnc.itc.security.dto.UserProfile;

import java.text.ParseException;

/**
 *
 */
public interface VertexCloudService {

	/**
	 * @param token Authentication token (JWT) sent by the client.
	 * @return User Profile returned from Vertex Cloud.
	 */
	UserProfile fetchUserProfile(String token) throws ParseException;

	/**
	 * @param token Authentication token (JWT) sent by the client.
	 * @return Tenant Profile returned from Vertex Cloud.
	 */
	TenantProfile fetchTenantProfile(String token);

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/service/impl/UserPermissionServiceImpl.java`

```java
package com.vertex.cnc.itc.security.service.impl;

import com.vertex.cnc.itc.security.dto.UserAccessPermissionResponseDTO;
import com.vertex.cnc.itc.security.service.UserPermissionService;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.io.Serializable;
import java.util.List;

@Service
@AllArgsConstructor
public class UserPermissionServiceImpl implements UserPermissionService {

    private final PermissionServiceImpl permissionServiceImpl;

    @Override
    public boolean hasPermission(String dataTestId, String permissionLevel) {
        List<UserAccessPermissionResponseDTO> permissions = permissionServiceImpl.getUserAccessPermissions();
        return permissions != null && !permissions.isEmpty() && permissions.stream()
                .anyMatch(p -> p.getDataTestId().equals(dataTestId)
                        && p.getPermissionLevel().equalsIgnoreCase(permissionLevel));
    }

    @Override
    public boolean hasPermissionByIdAndType(String username, Serializable targetId, String targetType,
            String permission) {

        List<UserAccessPermissionResponseDTO> permissions = permissionServiceImpl.getUserAccessPermissions();

        if (permissions == null || permissions.isEmpty()) {
            return false;
        }

        return permissions.stream()
                .anyMatch(p -> p.getDataTestId().equals(targetId.toString())
                        // && p.getTargetType().equalsIgnoreCase(targetType)
                        && p.getPermissionLevel().equalsIgnoreCase(permission));
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/service/impl/PermissionServiceImpl.java`

```java
package com.vertex.cnc.itc.security.service.impl;

import com.vertex.cnc.itc.common.aop.CNCITCContext;
import com.vertex.cnc.itc.security.dto.UserAccessPermissionResponseDTO;
import com.vertex.cnc.itc.security.service.PermissionService;
import jakarta.transaction.Transactional;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@Service
@Transactional
public class PermissionServiceImpl implements PermissionService {

    @Value("${cnc-itc.baseurl}")
    private String configUrl;
    private static final Logger logger = LogManager.getLogger(PermissionServiceImpl.class);
    private final RestTemplate restTemplate;


    public PermissionServiceImpl(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public List<UserAccessPermissionResponseDTO> getUserAccessPermissions() {
        String url = configUrl + "v1/user/permissions";
        HttpHeaders headers = new HttpHeaders();
        var token = CNCITCContext.getContext().getToken();
        if (token == null || token.isEmpty()) {
            logger.error("token is empty");
            return null;
        }
        headers.set("Authorization", CNCITCContext.getContext().getToken());
        HttpEntity<String> entity = new HttpEntity<>(headers);
        
        ResponseEntity<List<UserAccessPermissionResponseDTO>> response = restTemplate.exchange(
            url, HttpMethod.GET, entity, new ParameterizedTypeReference<List<UserAccessPermissionResponseDTO>>() {}
                );
        return response.getBody();
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/security/service/impl/VertexCloudServiceImpl.java`

```java
package com.vertex.cnc.itc.security.service.impl;

import com.nimbusds.jwt.JWTClaimsSet;
import com.nimbusds.jwt.JWTParser;
import com.vertex.cnc.itc.common.aop.CNCITCContext;
import com.vertex.cnc.itc.common.utility.WebClientUtils;
import com.vertex.cnc.itc.security.dto.Role;
import com.vertex.cnc.itc.security.dto.TenantProfile;
import com.vertex.cnc.itc.security.dto.UserProfile;
import com.vertex.cnc.itc.security.service.VertexCloudService;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.security.InvalidParameterException;
import java.text.ParseException;

@Service
public class VertexCloudServiceImpl implements VertexCloudService {

	private static final Logger logger = LogManager.getLogger(VertexCloudServiceImpl.class);

	private static final String NO_AUTHENTICATION_TOKEN_PROVIDED = "No authentication token provided.";

	@Value("${cloud.profile.url}")
	private String profileUri;

	/**
	 * Extract the "subject/sub" from JWT token.
	 * @param token Authentication token (JWT) sent by the client.
	 * @return
	 * @throws Exception
	 */
	@Override
	public UserProfile fetchUserProfile(String token) throws ParseException {
		if (token != null) {
			logger.debug("Fetching User Profile using token '{}'", token);
		}
		else {
			logger.error("Cannot fetch User Profile because the token is null");
			throw new InvalidParameterException(NO_AUTHENTICATION_TOKEN_PROVIDED);
		}
		JWTClaimsSet jwtClaimsSet = JWTParser.parse(token.split(" ")[1]).getJWTClaimsSet();
		String subject = jwtClaimsSet.getSubject();
		UserProfile userProfile = new UserProfile();
		userProfile.setSub(subject);
		return userProfile;
	}

	@Override
	public TenantProfile fetchTenantProfile(String token) {
		if (token != null) {
			logger.debug("Fetching Tenant Profile using token '{}'", token);
		}
		else {
			logger.error("Cannot fetch Tenant Profile because the token is null");
			throw new InvalidParameterException(NO_AUTHENTICATION_TOKEN_PROVIDED);
		}
		WebClientUtils webClientUtils = new WebClientUtils( new RestTemplate());
		TenantProfile tenantProfile = webClientUtils.performRestGet(token, profileUri, new ParameterizedTypeReference<TenantProfile>() {});
		setRoleAndFeaturesToContext(tenantProfile);
		return tenantProfile;

	}

	private void setRoleAndFeaturesToContext(TenantProfile tenantProfile) {
		if (tenantProfile.getSubscription() != null && tenantProfile.getRoles() != null) {
			CNCITCContext.getContext().setFeatures(tenantProfile.getSubscription().getFeatures());
			for (Role role : tenantProfile.getRoles()) {
				if (role.getUserRoleCode().equalsIgnoreCase("tta-itc-data-admin")) {
					CNCITCContext.getContext().setRole(role);
					break;
				}
			}
		}
	}
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/configuration/ApiExceptionHandler.java`

```java
package com.vertex.cnc.itc.configuration;

import com.vertex.cnc.itc.common.exception.ApiErrorResponse;
import com.vertex.cnc.itc.common.exception.ApiException;
import com.vertex.cnc.itc.common.exception.Errors;
import com.vertex.cnc.itc.common.exception.UnauthorizedAccessException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import java.time.LocalDateTime;
import java.util.stream.Collectors;

@ControllerAdvice
public class ApiExceptionHandler extends ResponseEntityExceptionHandler {

	private static final Logger LOG = LogManager.getLogger(ApiExceptionHandler.class);

	@Override
	protected ResponseEntity<Object> handleMethodArgumentNotValid(MethodArgumentNotValidException exception,
			HttpHeaders headers, HttpStatusCode status, WebRequest request) {
		LOG.error("ApiExceptionHandler caught exception for handleMethodArgumentNotValid", exception);

		String errorMessage = exception.getFieldErrors()
			.stream()
			.map(cv -> cv == null ? "null" : cv.getDefaultMessage())
			.collect(Collectors.joining(", "));
		String source = exception.getCause().toString();

		ApiErrorResponse apiErrorResponse = new ApiErrorResponse(HttpStatus.BAD_REQUEST, errorMessage, source);
		return new ResponseEntity<>(getErrorList(apiErrorResponse), HttpStatus.BAD_REQUEST);
	}

	@ExceptionHandler(AccessDeniedException.class)
	public final ResponseEntity<Object> handleAccessDeniedExceptions(AccessDeniedException exception) {
		LOG.warn("ApiExceptionHandler caught exception for handleAccessDeniedExceptions", exception);

		ApiErrorResponse apiErrorResponse = new ApiErrorResponse(HttpStatus.FORBIDDEN, exception.getMessage());

		return new ResponseEntity<>(getErrorList(apiErrorResponse), HttpStatus.FORBIDDEN);
	}

	@ExceptionHandler(Exception.class)
	public final ResponseEntity<Object> handleAllExceptions(Exception exception) {
		LOG.error("ApiExceptionHandler caught exception for handleAllExceptions", exception);

		ApiErrorResponse apiErrorResponse = new ApiErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR,
				exception.getMessage());
		return new ResponseEntity<>(getErrorList(apiErrorResponse), HttpStatus.INTERNAL_SERVER_ERROR);
	}

	@ExceptionHandler(ApiException.class)
	public ResponseEntity<Object> handleReportApiException(ApiException exception) {
		LOG.warn("ApiExceptionHandler caught exception for handleReportApiException", exception);

		ApiErrorResponse apiErrorResponse = new ApiErrorResponse(exception.getStatus(), exception.getMessage());
		return new ResponseEntity<>(getErrorList(apiErrorResponse), exception.getStatus());
	}

	@ExceptionHandler(DataIntegrityViolationException.class)
	public ResponseEntity<Object> handleDataIntegrityViolationException(DataIntegrityViolationException exception) {
		LOG.error("ApiExceptionHandler caught exception for handleDataIntegrityViolationException", exception);

		String source = exception.getCause().toString();
		ApiErrorResponse apiErrorResponse = new ApiErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR,
				"Data integrity violation", source);
		return new ResponseEntity<>(getErrorList(apiErrorResponse), HttpStatus.INTERNAL_SERVER_ERROR);
	}

	@ExceptionHandler(EmptyResultDataAccessException.class)
	public ResponseEntity<Object> handleEmptyResultDataAccessException(EmptyResultDataAccessException exception) {
		LOG.info("ApiExceptionHandler caught exception for handleEmptyResultDataAccessException", exception);

		String source = exception.getCause().toString();
		ApiErrorResponse apiErrorResponse = new ApiErrorResponse(HttpStatus.NO_CONTENT,
				"Requested Source System is Not Found", source);
		return new ResponseEntity<>(getErrorList(apiErrorResponse), HttpStatus.NO_CONTENT);
	}

	@ExceptionHandler(UnauthorizedAccessException.class)
	public final ResponseEntity<Object> handleUnauthorizedAccessException(UnauthorizedAccessException exception) {

		ApiErrorResponse apiErrorResponse = new ApiErrorResponse(exception.getMessage());
		return new ResponseEntity<>(getErrorList(apiErrorResponse), HttpStatus.UNAUTHORIZED);
	}

	private Errors getErrorList(ApiErrorResponse apiErrorResponse) {
		Errors errorList = new Errors();
		errorList.getError().add(apiErrorResponse);
		errorList.setTimestamp(LocalDateTime.now());
		return errorList;
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/configuration/SpringDocConfiguration.java`

```java
package com.vertex.cnc.itc.configuration;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.servers.Server;
import org.springdoc.core.models.GroupedOpenApi;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class SpringDocConfiguration {

	@Value("${cnc-itc.api.springdoc.server-name:http://localhost:8080/}")
	private String server;

	private static final String SECURITY_SCHEME_BEARER_AUTH = "Bearer Authentication";

	private SecurityScheme createAPISecurityScheme() {
		return new SecurityScheme().type(SecurityScheme.Type.HTTP)
				.name(SECURITY_SCHEME_BEARER_AUTH)
				.bearerFormat("JWT")
				.scheme("bearer");
	}

	@Bean
	public OpenAPI springDocOpenAPI() {
		Info information = new Info().title("Concourse ITC API").description("""
				<b>Description</b><br />
				<p>
				The configuration page lets users easily customize Concourse to fit their needs. Users
				can manage entity structures, set up periods, configure dashboards, and control user
				roles and permissions - all in one place.
				</p>

				<b>Additional Links</b><br />
				<ul>
				    <li>
				        <a href='' target='_blank'>Tax Data</a>
				    </li>
				    <li>
				        <a href='' target='_blank'>Tax Planning</a>
				    </li>
				    <li>
				        <a href='' target='_blank'>Audit Management</a>
				    </li>
				</ul>

				<b>Additional Urls</b><br />
				<ul>
				    <li>https://cnc-itc-api-dev.platdev.vtxdev.net/ - Dev Endpoint</li>
				    <li>https://cnc-itc-api-qa.platdev.vtxdev.net/ - QA Endpoint</li>
				    <li> - STAGE Endpoint</li>
				</ul>
				""").version("1.0.0");
		return new OpenAPI().info(information)
				.addSecurityItem(new SecurityRequirement().addList(SECURITY_SCHEME_BEARER_AUTH))
				.components(new Components().addSecuritySchemes(SECURITY_SCHEME_BEARER_AUTH,createAPISecurityScheme()))
				.addServersItem(new Server().url(server).description("CNC ITC Rest API"));
	}

	public static GroupedOpenApi buildGroupedOpenApi(String groupName, String[] packagesToScan) {
		return GroupedOpenApi.builder()
				.addOperationCustomizer(new SpringDocOperationCustomizer())
				.group(groupName)
				.packagesToScan(packagesToScan)
				.build();
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/configuration/SnowflakeDataSourceConfig.java`

```java
package com.vertex.cnc.itc.configuration;

import net.snowflake.client.jdbc.internal.org.bouncycastle.asn1.pkcs.PrivateKeyInfo;
import net.snowflake.client.jdbc.internal.org.bouncycastle.jce.provider.BouncyCastleProvider;
import net.snowflake.client.jdbc.internal.org.bouncycastle.openssl.PEMException;
import net.snowflake.client.jdbc.internal.org.bouncycastle.openssl.jcajce.JcaPEMKeyConverter;
import net.snowflake.client.pooling.SnowflakeConnectionPoolDataSource;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;
import java.security.PrivateKey;
import java.security.Security;
import java.util.Base64;

@Configuration
public class SnowflakeDataSourceConfig {
    private final SnowflakeConfiguration snowflakeConfiguration;

    public SnowflakeDataSourceConfig(final SnowflakeConfiguration snowflakeConfiguration) {
        this.snowflakeConfiguration = snowflakeConfiguration;
    }

    @Bean
    public DataSource dataSource() throws PEMException {
        var dataSource = new SnowflakeConnectionPoolDataSource();
        dataSource.setUrl(snowflakeConfiguration.getUrl());
        dataSource.setUser(snowflakeConfiguration.getUser());
        dataSource.setPrivateKey(decodePrivateKey(snowflakeConfiguration.getPrivateKey()));
        dataSource.setAuthenticator(snowflakeConfiguration.getAuthenticationType());
        return dataSource;
    }

    public static PrivateKey decodePrivateKey(final String privateKeyPem) throws PEMException {
        Security.addProvider(new BouncyCastleProvider());
        var cleanedPrivateKey = privateKeyPem
                .replace("-----BEGIN PRIVATE KEY-----", "")
                .replace("-----END PRIVATE KEY-----", "")
                .replaceAll("\\s+", "");

        var privateKeyBytes = Base64.getDecoder().decode(cleanedPrivateKey);
        var privateKeyInfo = PrivateKeyInfo.getInstance(privateKeyBytes);
        var converter = new JcaPEMKeyConverter().setProvider(BouncyCastleProvider.PROVIDER_NAME);
        return converter.getPrivateKey(privateKeyInfo);
    }

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/configuration/SnowflakeConfiguration.java`

```java
package com.vertex.cnc.itc.configuration;


import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;


@Component
@Getter
public class SnowflakeConfiguration {

    @Value("${cnc-itc.snowflake.database.user}")
    private String user;

    @Value("${cnc-itc.snowflake.database.private-key}")
    private String privateKey;

    @Value("${cnc-itc.snowflake.database.url}")
    private String url;

    @Value("${cnc-itc.snowflake.database.authentication-type}")
    private String authenticationType;

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/configuration/RequestResponseInterceptor.java`

```java
package com.vertex.cnc.itc.configuration;


import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpStatus;
import org.springframework.web.servlet.HandlerInterceptor;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Configuration
@RequiredArgsConstructor

public class RequestResponseInterceptor implements HandlerInterceptor {

    private static final Logger LOGGER = LoggerFactory.getLogger(RequestResponseInterceptor.class);
    private static final String CNC_ITC_API_ERROR_METRIC_NAME_VALUE = "CNC_API_ERROR_500";
    private static final String CNC_ITC_API_ERROR_METRIC_NAME_KEY = "CNC_API_ERROR_METRIC_NAME";
    private static final String CNC_ITC_API_RESPONSE_ERROR = "RESPONSE_ERROR";


    @Override
    public void afterCompletion(
            HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {

        if (response.getStatus() >= HttpStatus.INTERNAL_SERVER_ERROR.value()) {
            String msg = ex != null ? ex.getMessage() : "null exception";

            try(MDC.MDCCloseable key1 = MDC.putCloseable(CNC_ITC_API_ERROR_METRIC_NAME_KEY, CNC_ITC_API_ERROR_METRIC_NAME_VALUE);
                MDC.MDCCloseable key2 = MDC.putCloseable(CNC_ITC_API_RESPONSE_ERROR,msg);) {

                LOGGER.error("Response Status of afterCompletion method is {}.", response.getStatus(),ex);
            }
        }
    }

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/configuration/MvcWebConfiguration.java`

```java
package com.vertex.cnc.itc.configuration;

import jakarta.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
@RequiredArgsConstructor
public class MvcWebConfiguration implements WebMvcConfigurer {

	@Value("${cnc-itc.api.spring.cors.whitelist.mapping:/**}")
	private String whiteListMapping;

	@Value("${cnc-itc.api.spring.cors.whitelist.origins:*}")
	private String[] whiteListOrigins;

	@Value("${cnc-itc.api.spring.cors.whitelist.allowed.methods:*}")
	private String[] whiteListAllowedMethods;

	@Value("${cnc-itc.api.spring.cors.whitelist.maxage:1800}")
	private Long whiteListMaxAge;

	@Value("${cnc-itc.api.spring.cors.whitelist.allow.credentials:false}")
	private Boolean whiteListAllowCredentials;

	private final RequestResponseInterceptor requestResponseInterceptor;

	@Override
	public void addCorsMappings(@NotNull CorsRegistry registry) {
		registry.addMapping(whiteListMapping)
			.allowedOrigins(whiteListOrigins)
			.allowedMethods(whiteListAllowedMethods)
			.allowCredentials(whiteListAllowCredentials)
			.maxAge(whiteListMaxAge);
	}

	@Override
	public void addInterceptors(InterceptorRegistry registry) {
		registry.addInterceptor(requestResponseInterceptor);
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/configuration/SpringDocOperationCustomizer.java`

```java
package com.vertex.cnc.itc.configuration;

import io.swagger.v3.oas.models.Operation;
import org.springdoc.core.customizers.OperationCustomizer;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.method.HandlerMethod;

import java.util.Optional;

@Configuration
public class SpringDocOperationCustomizer implements OperationCustomizer {

	@Override
	public Operation customize(Operation operation, HandlerMethod handlerMethod) {
		Optional<PreAuthorize> preAuthorizeAnnotation = Optional
			.ofNullable(handlerMethod.getMethodAnnotation(PreAuthorize.class));
		boolean preAuthIsPresent = preAuthorizeAnnotation.isPresent();

		operation.setDescription(operation.getDescription() + "<br /><br />" + "Permissions -> "
				+ (preAuthIsPresent ? preAuthorizeAnnotation.get().value() : "None"));

		return operation;
	}

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/configuration/MethodSecurityConfig.java`

```java
package com.vertex.cnc.itc.configuration;

import com.vertex.cnc.itc.security.configuration.CustomPermissionEvaluator;
import com.vertex.cnc.itc.security.service.UserPermissionService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.security.access.expression.method.DefaultMethodSecurityExpressionHandler;
import org.springframework.security.access.expression.method.MethodSecurityExpressionHandler;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;

import static com.vertex.cnc.itc.common.constants.ApplicationConstants.NOT_TEST_PROFILE;

@Configuration
@EnableMethodSecurity(prePostEnabled = true)
@Profile(NOT_TEST_PROFILE)
public class MethodSecurityConfig {

    @Bean
    public MethodSecurityExpressionHandler methodSecurityExpressionHandler(UserPermissionService userPermissionService) {
        DefaultMethodSecurityExpressionHandler handler = new DefaultMethodSecurityExpressionHandler();
        handler.setPermissionEvaluator(new CustomPermissionEvaluator(userPermissionService));
        return handler;
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/models/Reports.java`

```java
package com.vertex.cnc.itc.taxabilityreview.models;

import com.vertex.cnc.itc.taxabilityreview.service.reports.ReportProvider;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class Reports {

    String reportCategory;
    List<DataView> reportList;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/models/DataView.java`

```java
package com.vertex.cnc.itc.taxabilityreview.models;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@AllArgsConstructor
public class DataView {
    String reportName;
    String description;
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/constants/ReportCategoryConstants.java`

```java
package com.vertex.cnc.itc.taxabilityreview.constants;

public class ReportCategoryConstants {

    public static final String VERTEX = "vertex";
    public static final String CUSTOM = "custom";
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/constants/ExceptionCodes.java`

```java
package com.vertex.cnc.itc.taxabilityreview.constants;

public class ExceptionCodes {
    public static final String MISSING_DATA_VIEW = "MISSING_DATA_VIEW";
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/configuration/ReportsConfiguration.java`

```java
package com.vertex.cnc.itc.taxabilityreview.configuration;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

import java.util.Map;

@PropertySource("classpath:taxabilityreview/taxability-reports.properties")
@ConfigurationProperties(prefix = "dataviews")
@Data
@Configuration
public class ReportsConfiguration {

    Map<String, String> categories;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/dto/ReportsRequestDTO.java`

```java
package com.vertex.cnc.itc.taxabilityreview.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.ZonedDateTime;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class ReportsRequestDTO {

    private ZonedDateTime startDate;

    private ZonedDateTime endDate;

    private String periodId;

    private String reportCategory;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/dto/ReportDataViewsResponse.java`

```java
package com.vertex.cnc.itc.taxabilityreview.dto;


import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class ReportDataViewsResponse {
    String key;
    String value;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/exceptions/MissingDataViewException.java`

```java
package com.vertex.cnc.itc.taxabilityreview.exceptions;

import com.vertex.cnc.itc.common.exception.ApiException;
import org.springframework.http.HttpStatus;

public class MissingDataViewException extends ApiException {
    private final String code;

    /**
     * Constructor for RecordNotFoundException
     * @param code - error code
     * @param message - error message
     */
    public MissingDataViewException(String code, String message) {
        super(HttpStatus.NOT_FOUND, message);
        this.code = code;
    }

    @Override
    public String getCode() { return code; }

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/controller/TaxabilityReviewController.java`

```java
package com.vertex.cnc.itc.taxabilityreview.controller;

import com.vertex.cnc.itc.common.ApiVersions;
import com.vertex.cnc.itc.common.RequestMappings;
import com.vertex.cnc.itc.taxabilityreview.dto.ReportDataViewsResponse;
import com.vertex.cnc.itc.taxabilityreview.dto.ReportsRequestDTO;
import com.vertex.cnc.itc.taxabilityreview.models.Reports;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.MediaType;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;


@Tag(
        name = "Taxability Review Canned Reports",
        description = """
                <b>Description</b><br />
                <p>
             
                </p>
                """)
@Validated
@RequestMapping(value = ApiVersions.V1 + RequestMappings.DATA_REVIEW)
@PreAuthorize("hasPermission('indirect-tax-close-menu-item', 'READ')")
public interface TaxabilityReviewController {

    @Operation(summary = "Fetches the static list of reports",
            description = "Retrieves list of reports, both vertex and any custom reports created by the user")
    @PostMapping(
            value = RequestMappings.REPORTS,
            produces = {MediaType.APPLICATION_JSON_VALUE})
    List<Reports> getAllReportsList(@Valid @RequestBody ReportsRequestDTO request);


    @Operation(summary = "Fetches dataview/report categories",
            description = "Retrieves list of report categories")
    @GetMapping(
            value = RequestMappings.REPORTVIEWS,
            produces = {MediaType.APPLICATION_JSON_VALUE})
    List<ReportDataViewsResponse>  getAllDataViews();

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/controller/impl/TaxabilityReviewControllerImpl.java`

```java
package com.vertex.cnc.itc.taxabilityreview.controller.impl;

import com.vertex.cnc.itc.taxabilityreview.dto.ReportDataViewsResponse;
import com.vertex.cnc.itc.taxabilityreview.dto.ReportsRequestDTO;
import com.vertex.cnc.itc.taxabilityreview.models.Reports;
import com.vertex.cnc.itc.taxabilityreview.service.TaxabilityReviewService;
import com.vertex.cnc.itc.taxabilityreview.controller.TaxabilityReviewController;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@AllArgsConstructor
public class TaxabilityReviewControllerImpl implements TaxabilityReviewController {

    private static final Logger LOGGER = LoggerFactory.getLogger(TaxabilityReviewControllerImpl.class);

    private final TaxabilityReviewService taxabilityReviewService;

    @Override
    public List<Reports> getAllReportsList(ReportsRequestDTO request) {
        LOGGER.debug("getTenantEntities");
        return taxabilityReviewService.getListOfAllReports(request);
    }

    @Override
    public List<ReportDataViewsResponse>  getAllDataViews() {
        LOGGER.debug("getAllDataViews");
        return taxabilityReviewService.getAllDataViews();
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/service/TaxabilityReviewService.java`

```java
package com.vertex.cnc.itc.taxabilityreview.service;

import com.vertex.cnc.itc.taxabilityreview.dto.ReportDataViewsResponse;
import com.vertex.cnc.itc.taxabilityreview.dto.ReportsRequestDTO;
import com.vertex.cnc.itc.taxabilityreview.models.Reports;

import java.util.List;

public interface TaxabilityReviewService {

    List<Reports> getListOfAllReports(ReportsRequestDTO request);
    List<ReportDataViewsResponse>  getAllDataViews();


}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/service/reports/CustomReportProvider.java`

```java
package com.vertex.cnc.itc.taxabilityreview.service.reports;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.vertex.cnc.itc.taxabilityreview.constants.ReportCategoryConstants;
import lombok.Data;
import org.springframework.stereotype.Component;

import java.util.List;

@Component(value = ReportCategoryConstants.CUSTOM)
@Data
public class CustomReportProvider implements ReportProvider {

    private String reportName;
    private String reportDescription;

    @JsonIgnore
    @Override
    public String getCategory() {
        return ReportCategoryConstants.CUSTOM;
    }

    @JsonIgnore
    @Override
    public List<CustomReportProvider> getList() {
        return null;
    }


    // Placeholder methods for the future.
    @JsonIgnore
    @Override
    public List<ReportProvider> allReports() {
        return null;
    }

    @JsonIgnore
    @Override
    public List<ReportProvider> reportSummary() {
        return null;
    }

    @JsonIgnore
    @Override
    public List<ReportProvider> reportDetails() {
        return null;
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/service/reports/ReportManager.java`

```java
package com.vertex.cnc.itc.taxabilityreview.service.reports;

import com.vertex.cnc.itc.taxabilityreview.configuration.ReportsConfiguration;
import com.vertex.cnc.itc.taxabilityreview.constants.ExceptionCodes;
import com.vertex.cnc.itc.taxabilityreview.exceptions.MissingDataViewException;
import com.vertex.cnc.itc.taxabilityreview.models.Reports;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.util.*;

@Component
public class ReportManager {
    private static final Logger LOGGER = LoggerFactory.getLogger(ReportManager.class);

    private Map<String, String> reportCategories;

    private final Map<String, ReportProvider> reportProviderMap = new HashMap<>();

    public ReportManager(List<ReportProvider> reportProviders, ReportsConfiguration reportsConfiguration) {
        this.reportCategories = reportsConfiguration.getCategories();
        for (ReportProvider provider : reportProviders) {
            reportProviderMap.put(provider.getCategory(), provider);
        }
    }

    public Map<String, String> getReportCategories() {
        if (Objects.isNull(reportCategories) || reportCategories.isEmpty() || !reportCategories.keySet().contains("vertex")) {
            throw new MissingDataViewException(ExceptionCodes.MISSING_DATA_VIEW, "Mandatory data view definitions are missing");
        }
        return reportCategories;
    }

    public List<Reports> getListofAllReports() {
        List<Reports> allReportsList = new ArrayList<>();
        for (String category : getReportCategories().keySet()) {
            ReportProvider provider = reportProviderMap.get(category);
            if (Objects.nonNull(provider)) {
                allReportsList.add(Reports.builder()
                        .reportCategory(category)
                        .reportList(provider.getList())
                        .build());
            } else {
                LOGGER.info("Report of category '" + category + "' not found");
            }
        }
        return allReportsList;
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/service/reports/VertexReportProvider.java`

```java
package com.vertex.cnc.itc.taxabilityreview.service.reports;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.vertex.cnc.itc.taxabilityreview.constants.ExceptionCodes;
import com.vertex.cnc.itc.taxabilityreview.constants.ReportCategoryConstants;
import com.vertex.cnc.itc.taxabilityreview.exceptions.MissingDataViewException;
import com.vertex.cnc.itc.taxabilityreview.models.DataView;
import com.vertex.cnc.itc.taxabilityreview.service.impl.TaxabilityReviewServiceImpl;
import lombok.Data;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.PropertySource;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Objects;

@PropertySource("classpath:taxabilityreview/taxability-reports.properties")
@ConfigurationProperties(prefix = "reports")
@Component(value = ReportCategoryConstants.VERTEX)
@Data
public class VertexReportProvider implements ReportProvider {
    private static final Logger LOGGER = LoggerFactory.getLogger(TaxabilityReviewServiceImpl.class);

    @JsonIgnore
    private List<DataView> vertexReportList;

    @Override
    @JsonIgnore
    public String getCategory() {
        return ReportCategoryConstants.VERTEX;
    }

    @Override
    @JsonIgnore
    public List<DataView> getList() {
        if(Objects.isNull(vertexReportList) || vertexReportList.isEmpty()) {
            LOGGER.error("Vertex report list is not configured");
            throw new MissingDataViewException(ExceptionCodes.MISSING_DATA_VIEW, "Mandatory report definitions are missing");
        }
        return vertexReportList;
    }

    // Placeholder methods for the future.
    @Override
    public List<ReportProvider> allReports() {
        return null;
    }

    @Override
    public List<ReportProvider> reportSummary() {
        return null;
    }

    @Override
    public List<ReportProvider> reportDetails() {
        return null;
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/service/reports/ReportProvider.java`

```java
package com.vertex.cnc.itc.taxabilityreview.service.reports;

import java.util.List;

public interface ReportProvider<T extends ReportProvider> {

    String getCategory();
    List<T> getList();
    List<ReportProvider> allReports();
    List<ReportProvider> reportSummary();
    List<ReportProvider> reportDetails();

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/taxabilityreview/service/impl/TaxabilityReviewServiceImpl.java`

```java
package com.vertex.cnc.itc.taxabilityreview.service.impl;

import com.vertex.cnc.itc.taxabilityreview.dto.ReportDataViewsResponse;
import com.vertex.cnc.itc.taxabilityreview.dto.ReportsRequestDTO;
import com.vertex.cnc.itc.taxabilityreview.models.Reports;
import com.vertex.cnc.itc.taxabilityreview.service.TaxabilityReviewService;
import com.vertex.cnc.itc.taxabilityreview.service.reports.ReportManager;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
@AllArgsConstructor
public class TaxabilityReviewServiceImpl implements TaxabilityReviewService {

    private static final Logger LOGGER = LoggerFactory.getLogger(TaxabilityReviewServiceImpl.class);
    ReportManager reportManager;

    @Override
    public List<Reports> getListOfAllReports(ReportsRequestDTO request) {
        return reportManager.getListofAllReports();
    }

    @Override
    public List<ReportDataViewsResponse> getAllDataViews() {
        Map<String, String> allReportCategories = reportManager.getReportCategories();

        List<ReportDataViewsResponse> allDataViews = new ArrayList<>();
        for (Map.Entry<String, String> entry : allReportCategories.entrySet()) {
            allDataViews.add(ReportDataViewsResponse.builder().key(entry.getKey()).value(entry.getValue()).build());
        }
        return allDataViews;
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dao/EntityDataReadinessCompletenessDao.java`

```java
package com.vertex.cnc.itc.datareadiness.dao;

import com.vertex.cnc.itc.datareadiness.dto.request.CompletenessRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.response.CompletenessPeriodResponseDTO;
import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessCompletenessDTO;

import java.util.List;

public interface EntityDataReadinessCompletenessDao {

	List<EntityDataReadinessCompletenessDTO> getCompletenessEntityResponse(String tenantId,
			CompletenessRequestDTO request);

	CompletenessPeriodResponseDTO getPeriodNumbers(String tenantId, CompletenessRequestDTO request);

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dao/EntityDao.java`

```java
package com.vertex.cnc.itc.datareadiness.dao;

import com.vertex.cnc.itc.datareadiness.dto.request.EntityRequestDTO;
import com.vertex.cnc.itc.datareadiness.response.DataReadinessSummary;

public interface EntityDao {
    DataReadinessSummary getTenantEntities(EntityRequestDTO request, String tenantId);
    void loadClientEntityPeriodItcStatus();
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dao/EntityDataReadinessDetailsDao.java`

```java
package com.vertex.cnc.itc.datareadiness.dao;

import com.vertex.cnc.itc.datareadiness.dto.request.EntityDetailsRequestDTO;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessDetails;

public interface EntityDataReadinessDetailsDao {
    EntityDataReadinessDetails getEntityDetailsResponse(String tenantId, EntityDetailsRequestDTO request);
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dao/impl/EntityDaoImpl.java`

```java
package com.vertex.cnc.itc.datareadiness.dao.impl;

import com.vertex.cnc.itc.datareadiness.configuration.EntityListQueryConfiguration;
import com.vertex.cnc.itc.datareadiness.constants.DataReadinessConstants;
import com.vertex.cnc.itc.datareadiness.dao.EntityDao;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessSummaryResponseDTO;
import com.vertex.cnc.itc.datareadiness.enums.DataReadinessStatusEnum;
import com.vertex.cnc.itc.datareadiness.mapper.EntityDataReadinessSummaryDTORowMapper;
import com.vertex.cnc.itc.datareadiness.response.DataReadinessSummary;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessSummary;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.env.Environment;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Component;

import java.sql.Timestamp;
import java.time.ZonedDateTime;

import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@Component("EntityDao")
@RequiredArgsConstructor
public class EntityDaoImpl implements EntityDao {

    private static final Logger LOGGER = LoggerFactory.getLogger(EntityDaoImpl.class);

    private final NamedParameterJdbcTemplate namedParameterJdbcTemplate;

    private final EntityDataReadinessSummaryDTORowMapper entityDataReadinessSummaryDTORowMapper;

    private final EntityListQueryConfiguration entityListQueryConfiguration;

    private final Environment environment;


    @Override
    public DataReadinessSummary getTenantEntities(EntityRequestDTO request, String tenantId) {
        LOGGER.debug("Getting tenant entities");
        List<EntityDataReadinessSummaryResponseDTO> entityResponseDTO = null;
        List<EntityDataReadinessSummary> entityDataReadinessSummaries = null;
        DataReadinessSummary dataReadinessSummary = new DataReadinessSummary();
        HashMap<String,Integer> counts =new HashMap<>();
        counts.put(DataReadinessStatusEnum.NOT_READY.getStatus(),0);
        counts.put(DataReadinessStatusEnum.NEEDS_REVIEW.getStatus(),0);
        counts.put(DataReadinessStatusEnum.VALIDATED_DATA.getStatus(),0);
        String env = getEnvironment();
        String entityListQuery = entityListQueryConfiguration.getEntityListQuery();
        String sql = String.format(entityListQuery, env, env);
        Map<String, Object> params = new HashMap<>();
        params.put(DataReadinessConstants.TENANT_ID, tenantId);
        params.put(DataReadinessConstants.PERIOD_ID, request.getPeriodId());
        params.put(DataReadinessConstants.START_DATE, convertToTimestamp(request.getStartDate()));
        params.put(DataReadinessConstants.END_DATE, convertToTimestamp(request.getEndDate()));
        try {
            entityResponseDTO = namedParameterJdbcTemplate
                    .queryForObject(sql, params, entityDataReadinessSummaryDTORowMapper);
            entityDataReadinessSummaries = convertToEntityDataReadinessSummary(entityResponseDTO);
            for (EntityDataReadinessSummary entity : entityDataReadinessSummaries) {
                String status = entity.getDataReadinessStatus();
                if (status == null) {
                    entity.setDataReadinessStatus(DataReadinessStatusEnum.NEEDS_REVIEW.getStatus());
                    status = DataReadinessStatusEnum.NEEDS_REVIEW.getStatus();
                }
                counts.put(status, counts.get(status) + 1);
                for (EntityDataReadinessSummary child : entity.getChildren()) {
                    String childStatus = child.getDataReadinessStatus();
                    if (childStatus == null) {
                        child.setDataReadinessStatus(DataReadinessStatusEnum.NEEDS_REVIEW.getStatus());
                        childStatus = DataReadinessStatusEnum.NEEDS_REVIEW.getStatus();
                    }
                    counts.put(childStatus, counts.get(childStatus) + 1);
                    for(EntityDataReadinessSummary grandChild : child.getChildren()) {
                        String grandChildStatus = grandChild.getDataReadinessStatus();
                        if (grandChildStatus == null) {
                            grandChild.setDataReadinessStatus(DataReadinessStatusEnum.NEEDS_REVIEW.getStatus());
                            grandChildStatus = DataReadinessStatusEnum.NEEDS_REVIEW.getStatus();
                        }
                        counts.put(grandChildStatus, counts.get(grandChildStatus) + 1);
                    }
                }
            }
            dataReadinessSummary.setStatusCounts(counts);
            dataReadinessSummary.setEntityDataReadinessSummaries(entityDataReadinessSummaries);
            //to do: sum up the status counts
        } catch (EmptyResultDataAccessException ex) {
            LOGGER.warn("No data found");
        }
        return dataReadinessSummary;
    }

    public void loadClientEntityPeriodItcStatus() {
        LOGGER.info("Loading client entity period ITC status");
        String env = getEnvironment();
        String sql = String.format(entityListQueryConfiguration.getClientEntityPeriodStatusQuery(), env, env, env, env, env);
        Map<String, Object> params = new HashMap<>();
        namedParameterJdbcTemplate.update(sql, params);

        LOGGER.info("Finished Loading client entity period ITC status");
    }

    public String getEnvironment() {
        String[] activeProfiles = environment.getActiveProfiles();
        switch (activeProfiles[0]) {
            case "local", "development" -> {
                return "DEV";
            }
            case "production" -> {
                return "PRD";
            }
            case "stage" -> {
                return "STG";
            }
            case "qa" -> {
                return "QA";
            }
        }

        return "DEV";
    }

    private static Timestamp convertToTimestamp(ZonedDateTime zonedDateTime) {
        return Optional.ofNullable(zonedDateTime)
                .map(ZonedDateTime::toInstant)
                .map(Timestamp::from)
                .orElse(null);
    }

    private static List<EntityDataReadinessSummary> convertToEntityDataReadinessSummary(List<EntityDataReadinessSummaryResponseDTO> entityResponseDTO) {
        Map<String, EntityDataReadinessSummary> entityMap = new HashMap<>();
        List<EntityDataReadinessSummary> rootEntities = new ArrayList<>();

        for (EntityDataReadinessSummaryResponseDTO entityData : entityResponseDTO) {
            EntityDataReadinessSummary finalEntity = EntityDataReadinessSummary.builder()
                    .entityId(entityData.getEntityId())
                    .entityName(entityData.getEntityName())
                    .parentEntityId(entityData.getParentEntityId())
                    .dataReadinessStatus(entityData.getDataReadinessStatus())
                    .children(new ArrayList<>())
                    .build();

            entityMap.put(finalEntity.getEntityId(), finalEntity);
        }
        for (EntityDataReadinessSummary finalEntity : entityMap.values()) {
            if (finalEntity.getParentEntityId() == null) {
                rootEntities.add(finalEntity);
            } else {
                EntityDataReadinessSummary parentEntity = entityMap.get(finalEntity.getParentEntityId());
                if (parentEntity != null) {
                    parentEntity.getChildren().add(finalEntity);
                }
            }
        }
        return rootEntities;
    }
}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dao/impl/EntityDataReadinessDetailsDaoImpl.java`

```java
package com.vertex.cnc.itc.datareadiness.dao.impl;

import com.vertex.cnc.itc.datareadiness.configuration.EntityDetailsQueryConfiguration;
import com.vertex.cnc.itc.datareadiness.constants.DataReadinessConstants;
import com.vertex.cnc.itc.datareadiness.dao.EntityDataReadinessDetailsDao;
import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessDetailsDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityDetailsRequestDTO;
import com.vertex.cnc.itc.datareadiness.mapper.TransactionDetailsRowMapper;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessDetails;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.env.Environment;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Component;

import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

@Component("EntityDetailsDao")
@RequiredArgsConstructor
public class EntityDataReadinessDetailsDaoImpl implements EntityDataReadinessDetailsDao {

    private static final Logger LOGGER = LoggerFactory.getLogger(EntityDataReadinessDetailsDaoImpl.class);

    private final EntityDetailsQueryConfiguration entityDetailsQueryConfiguration;

    private final TransactionDetailsRowMapper transactionDetailsRowMapper;

    private final NamedParameterJdbcTemplate namedParameterJdbcTemplate;

    private final Environment environment;

    @Override
    public EntityDataReadinessDetails getEntityDetailsResponse(String tenantId, EntityDetailsRequestDTO request) {
        LOGGER.info("Getting entity details for tenant, entity: {} {}", tenantId, request.getEntityId());
        // Fetch transaction details
        List<EntityDataReadinessDetailsDTO> transactionDetails = fetchTransactionDetails(tenantId, request);
        // Build response using transaction details
        EntityDataReadinessDetails response = buildEntityDataReadinessDetails(transactionDetails);
        response.setEntityId(request.getEntityId());
        response.setTenantId(tenantId);
        return response;
    }

    private List<EntityDataReadinessDetailsDTO> fetchTransactionDetails(String tenantId, EntityDetailsRequestDTO request) {
        List<EntityDataReadinessDetailsDTO> transactions = new ArrayList<>();
        Map<String, Object> params = new HashMap<>();
        params.put(DataReadinessConstants.TENANT_ID, tenantId);
        params.put(DataReadinessConstants.ENTITY_ID, request.getEntityId());
        params.put(DataReadinessConstants.START_DATE, convertToTimestamp(request.getStartDate()));
        params.put(DataReadinessConstants.END_DATE, convertToTimestamp(request.getEndDate()));
        try {
            String env = getEnvironment();
            String sql = String.format(entityDetailsQueryConfiguration.getEntityTransactionDetailsQuery(), env, env);
            transactions = namedParameterJdbcTemplate
                    .query(sql, params, transactionDetailsRowMapper);
        } catch (EmptyResultDataAccessException ex) {
            LOGGER.warn("No transaction data found for tenantId: {}", params.get(DataReadinessConstants.TENANT_ID));
        }
        return transactions;
    }


    private EntityDataReadinessDetails buildEntityDataReadinessDetails(List<EntityDataReadinessDetailsDTO> transactions) {
        // Default counts
        int totalTransactionsCount;
        int totalLinesCount = transactions.size();
        int successfulTransactionsCount;
        int successfulLinesCount = 0;
        int errorLinesCount = 0;

        // Count unique transactionidcodes + any NULL transactionidcode is counted as 1 transaction
        totalTransactionsCount = (int) transactions.stream()
                .map(EntityDataReadinessDetailsDTO::getTransactionIdCode)
                .filter(Objects::nonNull)
                .distinct()
                .count()
                + (transactions.stream().anyMatch(t -> t.getTransactionIdCode() == null) ? 1 : 0);

        // Map to track successful transactions
        Map<String, Boolean> transactionSuccessMap = new HashMap<>();
        List<String> errorMessagesList = new ArrayList<>();
        for (EntityDataReadinessDetailsDTO transaction : transactions) {
            if(transaction.getDfIsProcessed() == 0) {
                errorLinesCount++;
                errorMessagesList.add(transaction.getProcessingMessage());
            }
            if(transaction.getDfIsProcessed() == 1 || (transaction.getDfIsProcessed() >= 11 && transaction.getDfIsProcessed() <= 19)){
                successfulLinesCount++;
                if(transaction.getTransactionIdCode() != null)
                    transactionSuccessMap.putIfAbsent(transaction.getTransactionIdCode(), true);
                else
                    transactionSuccessMap.putIfAbsent("NULL", true);
            }else {
                // If any line in a transaction is not processed successfully, mark the entire transaction as failed
                if(transaction.getTransactionIdCode() == null){
                    transactionSuccessMap.put("NULL", false);
                }else{
                    transactionSuccessMap.put(transaction.getTransactionIdCode(), false);
                }
            }
        }
        successfulTransactionsCount = (int) transactionSuccessMap.values()
                .stream().filter(x -> x).count();

        return EntityDataReadinessDetails.builder()
                .totalTransactionsCount(totalTransactionsCount)
                .totalLinesCount(totalLinesCount)
                .successfulLinesCount(successfulLinesCount)
                .successfulTransactionsCount(successfulTransactionsCount)
                .errorLinesCount(errorLinesCount)
                .errorMessages(errorMessagesList)
                .build();

    }

    public String getEnvironment() {
        String[] activeProfiles = environment.getActiveProfiles();
        switch (activeProfiles[0]) {
            case "local", "development" -> {
                return "DEV";
            }
            case "production" -> {
                return "PRD";
            }
            case "stage" -> {
                return "STG";
            }
            case "qa" -> {
                return "QA";
            }
        }

        return "DEV";
    }

    private static String convertToTimestamp(ZonedDateTime zonedDateTime) {
        return Optional.ofNullable(zonedDateTime)
                .map(date -> date.format(DateTimeFormatter.ofPattern("yyyy-MM-dd")))
                .orElse(null);
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dao/impl/EntityDataReadinessCompletenessDaoImpl.java`

```java
package com.vertex.cnc.itc.datareadiness.dao.impl;


import com.vertex.cnc.itc.datareadiness.configuration.EntityCompletenessQueryConfiguration;
import com.vertex.cnc.itc.datareadiness.constants.DataReadinessConstants;
import com.vertex.cnc.itc.datareadiness.dao.EntityDataReadinessCompletenessDao;
import com.vertex.cnc.itc.datareadiness.dto.request.CompletenessRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.response.CompletenessPeriodResponseDTO;
import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessCompletenessDTO;
import com.vertex.cnc.itc.datareadiness.mapper.EntityDataReadinessCompletenessRowMapper;
import com.vertex.cnc.itc.datareadiness.mapper.PeriodNumberRowMapper;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Component;

import java.sql.Date;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Component("EntityDataReadinessCompletenessDao")
@RequiredArgsConstructor
public class EntityDataReadinessCompletenessDaoImpl implements EntityDataReadinessCompletenessDao {

	private static final Logger LOGGER = LoggerFactory.getLogger(EntityDataReadinessCompletenessDaoImpl.class);

	@Value("${cnc-itc.db.names.cnc-config}")
	private String cncConfigDb;

	@Value("${cnc-itc.db.names.datahub-semantic}")
	private String dataHubSemanticDb; //

	private final NamedParameterJdbcTemplate namedParameterJdbcTemplate;

	private final EntityCompletenessQueryConfiguration entityCompletenessQueryConfiguration;

	private final EntityDataReadinessCompletenessRowMapper entityDataReadinessCompletenessRowMapper;

	private final PeriodNumberRowMapper periodNumberRowMapper;

	@Override
	public List<EntityDataReadinessCompletenessDTO> getCompletenessEntityResponse(String tenantId,
			CompletenessRequestDTO request) {
		List<EntityDataReadinessCompletenessDTO> transactions = new ArrayList<>();
		Map<String, Object> params = new HashMap<>();
		params.put(DataReadinessConstants.TENANT_ID, tenantId);
		params.put(DataReadinessConstants.ENTITY_ID, request.getEntityId());
		params.put(DataReadinessConstants.START_DATE, Date.valueOf(request.getStartDate()));
		params.put(DataReadinessConstants.END_DATE, Date.valueOf(request.getEndDate()));

		try {
			String sql = String.format(entityCompletenessQueryConfiguration.getEntityCompletenessQuery()
					,cncConfigDb, cncConfigDb, cncConfigDb, dataHubSemanticDb, dataHubSemanticDb);
			LOGGER.debug("SQL: {}", sql);
			transactions = namedParameterJdbcTemplate.query(sql, params, entityDataReadinessCompletenessRowMapper);
		}
		catch (EmptyResultDataAccessException ex) {
			LOGGER.warn("No completeness data found for tenantId: {}", params.get(DataReadinessConstants.TENANT_ID));
		}
		return transactions;
	}

	@Override
	public CompletenessPeriodResponseDTO getPeriodNumbers(String tenantId, CompletenessRequestDTO request) {
		CompletenessPeriodResponseDTO response = new CompletenessPeriodResponseDTO();
		Map<String, Object> params = new HashMap<>();
		params.put(DataReadinessConstants.TENANT_ID, tenantId);
		params.put(DataReadinessConstants.START_DATE, Date.valueOf(request.getStartDate()));
		params.put(DataReadinessConstants.END_DATE, Date.valueOf(request.getEndDate()));

		try {
			String sql = String.format(entityCompletenessQueryConfiguration.getPeriodNumberQuery(), cncConfigDb,
					cncConfigDb, cncConfigDb, cncConfigDb);
			LOGGER.debug("Period Number SQL: {}", sql);
			response = namedParameterJdbcTemplate.queryForObject(sql, params, periodNumberRowMapper);
		}
		catch (EmptyResultDataAccessException ex) {
			LOGGER.warn("No Period Numbers found for tenantId: {}", params.get(DataReadinessConstants.TENANT_ID));
		}
		return response;

	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/constants/DataReadinessConstants.java`

```java
package com.vertex.cnc.itc.datareadiness.constants;

public class DataReadinessConstants {
    public static final String TENANT_ID = "tenantId";
    public  static final String ENTITY_ID = "entityId";
    public  static final String PERIOD_ID = "periodId";
    public static final String START_DATE = "startDate";
    public static final String END_DATE = "endDate";
    public static final String ENTITY_CODE = "entityCode";
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/configuration/EntityDetailsQueryConfiguration.java`

```java
package com.vertex.cnc.itc.datareadiness.configuration;

import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Configuration("EntityDetailsQueryConfiguration ")
@PropertySource("classpath:db/snowflake/datareadiness/entity-details-query.properties")
@Getter
@NoArgsConstructor
public class EntityDetailsQueryConfiguration {

    @Value("${entity-transaction-details.query}")
    private String entityTransactionDetailsQuery;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/configuration/EntityListQueryConfiguration.java`

```java
package com.vertex.cnc.itc.datareadiness.configuration;

import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Configuration("EntityListQueryConfiguration")
@PropertySource("classpath:db/snowflake/datareadiness/entity-list-query.properties")
@Getter
@NoArgsConstructor
public class EntityListQueryConfiguration {

    @Value("${entity-list.query}")
    private String entityListQuery;

    @Value("${client-entity-period-status.query}")
    private String clientEntityPeriodStatusQuery;

}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/configuration/EntityCompletenessQueryConfiguration.java`

```java
package com.vertex.cnc.itc.datareadiness.configuration;

import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Configuration("EntityCompletenessQueryConfiguration ")
@PropertySource("classpath:db/snowflake/datareadiness/completeness-query.properties")
@Getter
@NoArgsConstructor
public class EntityCompletenessQueryConfiguration {

    @Value("${completeness-details.query}")
    private String entityCompletenessQuery;

	@Value("${tenantperiodnumbers.query}")
	private String periodNumberQuery;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dto/request/EntityDetailsRequestDTO.java`

```java
package com.vertex.cnc.itc.datareadiness.dto.request;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import net.snowflake.client.jdbc.internal.joda.time.LocalDate;

import java.time.ZonedDateTime;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class EntityDetailsRequestDTO {

    @NotNull
    private ZonedDateTime startDate;

    @NotNull
    private ZonedDateTime endDate;

    @NotNull
    private String entityId;

}


```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dto/request/EntityRequestDTO.java`

```java
package com.vertex.cnc.itc.datareadiness.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.ZonedDateTime;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class EntityRequestDTO {

    private ZonedDateTime startDate;

    private ZonedDateTime endDate;

    private String periodId;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dto/request/CompletenessRequestDTO.java`

```java
package com.vertex.cnc.itc.datareadiness.dto.request;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class CompletenessRequestDTO {

	@NotNull
	private LocalDate startDate;

	@NotNull
	private LocalDate endDate;

	@NotNull
	private String entityId;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dto/response/EntityDataReadinessDetailsDTO.java`

```java
package com.vertex.cnc.itc.datareadiness.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class EntityDataReadinessDetailsDTO {
    private String tenantId;
    private String transactionIdCode;
    private String lineItemIdCode;
    private String lineItemNumber;
    private String postingDate;
    private Integer dfIsProcessed;
    private String processingMessage;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dto/response/EntityDataReadinessCompletenessDTO.java`

```java
package com.vertex.cnc.itc.datareadiness.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class EntityDataReadinessCompletenessDTO {

	private String completenessCategory;

	private BigDecimal previousPeriodTotal;

	private BigDecimal currentPeriodTotal;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dto/response/CompletenessResponseDTO.java`

```java
package com.vertex.cnc.itc.datareadiness.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class CompletenessResponseDTO {
    private BigDecimal basisTransactionsTotal;
    private BigDecimal taxTransactionsTotal;
}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dto/response/CompletenessPeriodResponseDTO.java`

```java
package com.vertex.cnc.itc.datareadiness.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class CompletenessPeriodResponseDTO {

	private Integer currentPeriodNumber;

	private Integer previousPeriodNumber;

	private LocalDate startDatePrevious;

	private LocalDate endDatePrevious;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/dto/response/EntityDataReadinessSummaryResponseDTO.java`

```java
package com.vertex.cnc.itc.datareadiness.dto.response;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;


@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class EntityDataReadinessSummaryResponseDTO {

    private String entityId;

    private String entityName;

    private String parentEntityId;

    private String dataReadinessStatus;

    private Integer hierarchyLevel;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/mapper/EntityDataReadinessSummaryDTORowMapper.java`

```java
package com.vertex.cnc.itc.datareadiness.mapper;

import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessSummaryResponseDTO;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Component;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

@Component
public class EntityDataReadinessSummaryDTORowMapper implements RowMapper<List<EntityDataReadinessSummaryResponseDTO>> {
    @Override
    public List<EntityDataReadinessSummaryResponseDTO> mapRow(ResultSet rs, int rowNum) throws SQLException {
        List<EntityDataReadinessSummaryResponseDTO> entityDataReadinessSummaryResponseDTOList = new ArrayList<>();
        do {
            EntityDataReadinessSummaryResponseDTO entityDataReadinessSummaryResponseDTO = EntityDataReadinessSummaryResponseDTO.builder()
                    .entityId(rs.getString("ENTITY_ID"))
                    .entityName(rs.getString("ENTITY_NAME"))
                    .parentEntityId(rs.getString("PARENT_ENTITY_ID"))
                    .dataReadinessStatus(rs.getString("DATA_READINESS_STATUS"))
                    .build();
            entityDataReadinessSummaryResponseDTOList.add(entityDataReadinessSummaryResponseDTO);
        } while (rs.next());
        return entityDataReadinessSummaryResponseDTOList;
    }
}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/mapper/TransactionDetailsRowMapper.java`

```java
package com.vertex.cnc.itc.datareadiness.mapper;

import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessDetailsDTO;

import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Component;

import java.sql.ResultSet;
import java.sql.SQLException;

@Component
public class TransactionDetailsRowMapper implements RowMapper<EntityDataReadinessDetailsDTO> {
    @Override
    public EntityDataReadinessDetailsDTO mapRow(ResultSet rs, int rowNum) throws SQLException {
        return EntityDataReadinessDetailsDTO.builder()
                .tenantId(rs.getString("TENANT_ID"))
                .transactionIdCode(rs.getString("TRANSACTION_ID"))
                .lineItemIdCode(rs.getString("LINE_ITEM_ID"))
                .lineItemNumber(rs.getString("LINE_ITEM_NUMBER"))
                .postingDate(rs.getString("POSTING_DATE"))
                .dfIsProcessed(rs.getInt("DF_IS_PROCESSED"))
                .processingMessage(rs.getString("PROCESSING_MESSAGE"))
                .build();
    }
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/mapper/PeriodNumberRowMapper.java`

```java
package com.vertex.cnc.itc.datareadiness.mapper;

import com.vertex.cnc.itc.datareadiness.dto.response.CompletenessPeriodResponseDTO;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Component;

import java.sql.ResultSet;
import java.sql.SQLException;

@Component

public class PeriodNumberRowMapper implements RowMapper<CompletenessPeriodResponseDTO> {

	@Override
	public CompletenessPeriodResponseDTO mapRow(ResultSet rs, int rowNum)
			throws SQLException {
		return CompletenessPeriodResponseDTO.builder()
			.currentPeriodNumber(rs.getInt("CURRENT_PERIOD_NUMBER"))
			.previousPeriodNumber(rs.getInt("PREVIOUS_PERIOD_NUMBER"))
			.startDatePrevious(rs.getDate("PREVIOUS_STARTDATE").toLocalDate())
			.endDatePrevious(rs.getDate("PREVIOUS_ENDDATE").toLocalDate())
			.build();
	}
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/mapper/EntityDataReadinessCompletenessRowMapper.java`

```java
package com.vertex.cnc.itc.datareadiness.mapper;

import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessCompletenessDTO;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Component;

import java.sql.ResultSet;
import java.sql.SQLException;

@Component
public class EntityDataReadinessCompletenessRowMapper implements RowMapper<EntityDataReadinessCompletenessDTO> {

	@Override
	public EntityDataReadinessCompletenessDTO mapRow(ResultSet rs, int rowNum) throws SQLException {
		return EntityDataReadinessCompletenessDTO.builder()
			.completenessCategory(rs.getString("CATEGORY"))
			.previousPeriodTotal(rs.getBigDecimal("PREVIOUS_PERIOD_TOTAL"))
			.currentPeriodTotal(rs.getBigDecimal("CURRENT_PERIOD_TOTAL"))
			.build();
	}

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/response/TxLineErrorCode.java`

```java
package com.vertex.cnc.itc.datareadiness.response;

import lombok.Getter;

@Getter
public enum TxLineErrorCode {
    // TODO: Validate these enums once we have more details
    NOT_VALIDATED(1001),
    NOT_STANDARDIZED(1002),
    MISSING_FIELDS(1003);

    private final int code;

    TxLineErrorCode(int code) {
        this.code = code;
    }

    public static TxLineErrorCode fromCode(int code) {
        for (TxLineErrorCode errorCode : values()) {
            if (errorCode.code == code) {
                return errorCode;
            }
        }
        throw new IllegalArgumentException("Invalid error code: " + code);
    }
}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/response/EntityDataReadinessSummary.java`

```java
package com.vertex.cnc.itc.datareadiness.response;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class EntityDataReadinessSummary {
    String entityName;
    String entityId;
    String dataReadinessStatus;
    String parentEntityId;
    List<EntityDataReadinessSummary> children;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/response/EntityDataCompletenessDetail.java`

```java
package com.vertex.cnc.itc.datareadiness.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class EntityDataCompletenessDetail {

	private String completenessCategory;

	private BigDecimal previousPeriodTotal;

	private BigDecimal currentPeriodTotal;

	private BigDecimal differencePercentage;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/response/EntityDataCompleteness.java`

```java
package com.vertex.cnc.itc.datareadiness.response;

import com.vertex.cnc.itc.datareadiness.enums.CompletenessCategory;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class EntityDataCompleteness {

	private Integer currentPeriodNumber;

	private Integer previousPeriodNumber;

	private LocalDate currentPeriodStartDate;

	private LocalDate currentPeriodEndDate;

	private LocalDate previousPeriodStartDate;

	private LocalDate previousPeriodEndDate;

	@Builder.Default
	Map<CompletenessCategory, List<EntityDataCompletenessDetail>> entityDataCompletenessDetails = new EnumMap<>(
			CompletenessCategory.class);

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/response/DataReadinessSummary.java`

```java
package com.vertex.cnc.itc.datareadiness.response;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class DataReadinessSummary {
    Map<String, Integer> statusCounts;
    List<EntityDataReadinessSummary> entityDataReadinessSummaries;

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/response/EntityDataReadinessDetails.java`

```java
package com.vertex.cnc.itc.datareadiness.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class EntityDataReadinessDetails {
    private String tenantId;
    private String entityId;
    private Integer totalTransactionsCount;
    private Integer totalLinesCount;
    private Integer successfulTransactionsCount;
    private Integer successfulLinesCount;
    private Integer errorLinesCount;
    @Builder.Default
    private Map<TxLineErrorCode, Integer> errorCountPerCategory = new EnumMap<>(TxLineErrorCode.class);
    private List<String> errorMessages;
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/controller/DataReadinessController.java`

```java
package com.vertex.cnc.itc.datareadiness.controller;

import com.vertex.cnc.itc.common.ApiVersions;
import com.vertex.cnc.itc.common.RequestMappings;
import com.vertex.cnc.itc.datareadiness.dto.request.CompletenessRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityDetailsRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityRequestDTO;
import com.vertex.cnc.itc.datareadiness.response.EntityDataCompleteness;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessDetails;
import com.vertex.cnc.itc.datareadiness.response.DataReadinessSummary;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.MediaType;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@Tag(
        name = "Data Readiness",
        description = """
                <b>Description</b><br />
                <p>
                Indirect Tax Close is a transaction tax accounting application to govern and execute period end with confidence.

                The Data Readiness Dashboard displays the data readiness and tax close statuses for entities in the
                selected filing period. You can view the total list of entities, entities that need data reviewed,
                or entities moved to tax close.
                </p>
                                
                <b>Additional Links</b><br />
                <ul>
                    <li>
                        <a href=' replace this https://vertexinc.atlassian.net/wiki/spaces/ITI/pages/3253144015/Sales+
                        Accuracy+Risk+Dashboard' target='_blank'>ITC - Data Readiness Dashboard </a>
                    </li>
                </ul>
                """)
@Validated
@RequestMapping(value = ApiVersions.V1 + RequestMappings.DATA_READINESS)
@PreAuthorize("hasPermission('data-readiness-menu-item', 'READ')")
public interface DataReadinessController {

    @Operation(summary = "Fetches the tenant's Entity data and data readiness counts",
            description = "Retrieves list of entities")
    @PostMapping(
            value = RequestMappings.ENTITIES ,
            produces = {MediaType.APPLICATION_JSON_VALUE})
    DataReadinessSummary getTenantEntities(@Valid @RequestBody EntityRequestDTO request);

    @Operation(summary = "Fetches an Entity's details", description = "Retrieves details from the selected entity")
    @PostMapping(
            value = RequestMappings.ENTITY,
            produces = {MediaType.APPLICATION_JSON_VALUE})
    EntityDataReadinessDetails getEntityDataReadinessDetails(@Valid @RequestBody EntityDetailsRequestDTO request);


    @Operation(summary = "Fetches the Entity's completeness data", description = "Retrieves completeness information")
    @PostMapping(
            value = RequestMappings.COMPLETENESS ,
            produces = {MediaType.APPLICATION_JSON_VALUE})
    EntityDataCompleteness getEntityCompleteness(@Valid @RequestBody CompletenessRequestDTO request);
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/controller/impl/DataReadinessControllerImpl.java`

```java
package com.vertex.cnc.itc.datareadiness.controller.impl;

import com.vertex.cnc.itc.common.exception.ApiException;
import com.vertex.cnc.itc.datareadiness.controller.DataReadinessController;
import com.vertex.cnc.itc.datareadiness.dto.request.CompletenessRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityDetailsRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityRequestDTO;
import com.vertex.cnc.itc.datareadiness.response.EntityDataCompleteness;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessDetails;
import com.vertex.cnc.itc.datareadiness.response.DataReadinessSummary;
import com.vertex.cnc.itc.datareadiness.service.DataReadinessService;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.RestController;

@RestController
@AllArgsConstructor
public class DataReadinessControllerImpl implements DataReadinessController {

    private static final Logger LOGGER = LoggerFactory.getLogger(DataReadinessControllerImpl.class);

    private final DataReadinessService dataReadinessService;

    @Override
    public DataReadinessSummary getTenantEntities(EntityRequestDTO request) {
        LOGGER.debug("Controller method getTenantEntities invoked");
        try{
            return dataReadinessService.getTenantEntities(request);
        } catch (Exception e) {
            LOGGER.error("Error occurred while fetching tenant entities", e);
            throw new ApiException("Error occurred while fetching tenant entities"+ e);
        }
    }

    @Override
    public EntityDataReadinessDetails getEntityDataReadinessDetails(EntityDetailsRequestDTO request) {
        LOGGER.debug("Controller method getEntityDetails invoked");
        try{
            return dataReadinessService.getEntityDetails(request);
        } catch (Exception e) {
            LOGGER.error("Error occurred while fetching entity details", e);
            throw new ApiException("Error occurred while fetching entity details");
        }
    }

    @Override
    public EntityDataCompleteness getEntityCompleteness(CompletenessRequestDTO request) {
        LOGGER.debug("Controller method getEntityCompleteness invoked");
        try{
            return dataReadinessService.getCompletenessEntityDetails(request);
        } catch (Exception e) {
            LOGGER.error("Error occurred while fetching Completeness entity details", e);
            throw new ApiException("Error occurred while fetching entity details");
        }
    }
}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/service/DataReadinessService.java`

```java
package com.vertex.cnc.itc.datareadiness.service;

import com.vertex.cnc.itc.datareadiness.dto.request.CompletenessRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityDetailsRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityRequestDTO;
import com.vertex.cnc.itc.datareadiness.response.EntityDataCompleteness;
import com.vertex.cnc.itc.datareadiness.response.DataReadinessSummary;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessDetails;

public interface DataReadinessService {
    DataReadinessSummary getTenantEntities(EntityRequestDTO request);
    EntityDataReadinessDetails getEntityDetails(EntityDetailsRequestDTO request);
    void loadClientEntityPeriodItcStatus();

    EntityDataCompleteness getCompletenessEntityDetails(CompletenessRequestDTO request);
}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/service/impl/DataReadinessServiceImpl.java`

```java
package com.vertex.cnc.itc.datareadiness.service.impl;

import com.vertex.cnc.itc.common.aop.CNCITCContext;
import com.vertex.cnc.itc.common.constants.ApplicationConstants;
import com.vertex.cnc.itc.common.exception.RecordNotFoundException;
import com.vertex.cnc.itc.datareadiness.dao.impl.EntityDaoImpl;
import com.vertex.cnc.itc.datareadiness.dao.impl.EntityDataReadinessCompletenessDaoImpl;
import com.vertex.cnc.itc.datareadiness.dao.impl.EntityDataReadinessDetailsDaoImpl;
import com.vertex.cnc.itc.datareadiness.dto.request.CompletenessRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityDetailsRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.request.EntityRequestDTO;
import com.vertex.cnc.itc.datareadiness.dto.response.CompletenessPeriodResponseDTO;
import com.vertex.cnc.itc.datareadiness.dto.response.EntityDataReadinessCompletenessDTO;
import com.vertex.cnc.itc.datareadiness.enums.CompletenessCategory;
import com.vertex.cnc.itc.datareadiness.response.EntityDataCompleteness;
import com.vertex.cnc.itc.datareadiness.response.DataReadinessSummary;
import com.vertex.cnc.itc.datareadiness.response.EntityDataCompletenessDetail;
import com.vertex.cnc.itc.datareadiness.response.EntityDataReadinessDetails;
import com.vertex.cnc.itc.datareadiness.service.DataReadinessService;
import com.vertex.cnc.itc.security.dto.TenantProfile;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@AllArgsConstructor
public class DataReadinessServiceImpl implements DataReadinessService {

    private static final Logger LOGGER = LoggerFactory.getLogger(DataReadinessServiceImpl.class);

    private final EntityDaoImpl entityDaoImpl;

    private final EntityDataReadinessDetailsDaoImpl entityDataReadinessDetailsDaoImpl;

	private final EntityDataReadinessCompletenessDaoImpl entityDataReadinessCompletenessDaoImpl;

	public DataReadinessSummary getTenantEntities(EntityRequestDTO request) {
        return Optional.ofNullable(CNCITCContext.getContext().getTenantProfile())
                .map(TenantProfile::getTenantId)
                .map(tenantId -> {
                    return entityDaoImpl.getTenantEntities(request, tenantId);
                })
                .orElseThrow(() -> {
                    String msg = String.format("No entities found for tenantId: %s",
                            CNCITCContext.getContext().getTenantProfile().getTenantId());
                    LOGGER.error(msg);
                    return new RecordNotFoundException(ApplicationConstants.RECORD_NOT_FOUND_CODE, msg);
                });
    }

    public EntityDataReadinessDetails getEntityDetails(EntityDetailsRequestDTO request) {
        return Optional.ofNullable(CNCITCContext.getContext().getTenantProfile())
                .map(TenantProfile::getTenantId)
                .map(tenantId ->
                        entityDataReadinessDetailsDaoImpl.getEntityDetailsResponse(
                                tenantId,
                                request
                        ))
                .orElseThrow(() -> {
                    String msg = String.format("Entity details not found for tenantId: %s, entityId: %s",
                            CNCITCContext.getContext().getTenantProfile().getTenantId(),
                            request.getEntityId());
                    LOGGER.error(msg);
                    return new RecordNotFoundException(ApplicationConstants.RECORD_NOT_FOUND_CODE, msg);
                });

    }
    @Scheduled(cron = "0 0 6 ? * *"
            , zone = "UTC")
    public void loadClientEntityPeriodItcStatus() {
        entityDaoImpl.loadClientEntityPeriodItcStatus();
    }

	public EntityDataCompleteness getCompletenessEntityDetails(CompletenessRequestDTO request) {
		return Optional.ofNullable(CNCITCContext.getContext().getTenantProfile())
				.map(TenantProfile::getTenantId)
				.map(tenantId -> {
					List<EntityDataReadinessCompletenessDTO> completenessData = entityDataReadinessCompletenessDaoImpl
							.getCompletenessEntityResponse(tenantId, request);

					CompletenessPeriodResponseDTO periodNumbersData = entityDataReadinessCompletenessDaoImpl
							.getPeriodNumbers(tenantId, request);
					Integer	currentPeriodNumber = 0;
					Integer	previousPeriodNumber = 0;
					LocalDate previousPeriodStartDate = periodNumbersData.getStartDatePrevious();
					LocalDate previousPeriodEndDate = periodNumbersData.getEndDatePrevious();

					if (periodNumbersData.getCurrentPeriodNumber() != null ) {
						currentPeriodNumber = periodNumbersData.getCurrentPeriodNumber();
						previousPeriodNumber = periodNumbersData.getPreviousPeriodNumber();
					}

					List<EntityDataCompletenessDetail> completenessDetails = completenessData
							.stream().map(datadetails -> {
								BigDecimal diffPercentage = new BigDecimal(0.0);
								if (datadetails.getPreviousPeriodTotal().compareTo(BigDecimal.ZERO) != 0) {
									BigDecimal difference = datadetails.getCurrentPeriodTotal().subtract(datadetails.getPreviousPeriodTotal());
									BigDecimal roundedPercentage = difference.divide(datadetails.getPreviousPeriodTotal(),
											10, BigDecimal.ROUND_HALF_UP).abs().multiply(new BigDecimal("100"));

									diffPercentage  = roundedPercentage.setScale(2, RoundingMode.HALF_UP);

								}
								return EntityDataCompletenessDetail.builder()
										.completenessCategory(datadetails.getCompletenessCategory())
										.previousPeriodTotal(datadetails.getPreviousPeriodTotal())
										.currentPeriodTotal(datadetails.getCurrentPeriodTotal())
										.differencePercentage(diffPercentage)
										.build();
							}).collect(Collectors.toList());

					Map<CompletenessCategory, List<EntityDataCompletenessDetail>> groupedByCategory = completenessDetails
							.stream()
							.collect(Collectors
									.groupingBy(dto -> CompletenessCategory.valueOf(dto.getCompletenessCategory().toUpperCase())));

					return EntityDataCompleteness.builder()
							.currentPeriodStartDate(request.getStartDate())
							.currentPeriodNumber(currentPeriodNumber)
							.previousPeriodNumber(previousPeriodNumber)
							.currentPeriodEndDate(request.getEndDate())
							.previousPeriodStartDate(previousPeriodStartDate)
							.previousPeriodEndDate(previousPeriodEndDate)
							.entityDataCompletenessDetails(groupedByCategory)
							.build();
				})
				.orElseThrow(() -> {
					String msg = String.format("Completeness details not found for tenantId: %s, entityId: %s",
							CNCITCContext.getContext().getTenantProfile().getTenantId(), request.getEntityId());
					LOGGER.error(msg);
					return new RecordNotFoundException(ApplicationConstants.RECORD_NOT_FOUND_CODE, msg);
				});
	}
}
```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/enums/DataReadinessStatusEnum.java`

```java
package com.vertex.cnc.itc.datareadiness.enums;

/**
 * Enum to define DataReadinessStatus.
 */
public enum DataReadinessStatusEnum {

    NOT_READY("Not Ready"),
    NEEDS_REVIEW("Needs Review"),
    VALIDATED_DATA("Validated Data");

    DataReadinessStatusEnum(String status) { this.status = status; }
    private String status;
    public String getStatus() { return this.status; }

}

```

## 📄 `../vertexinc/cnc-itc-api/src/main/java/com/vertex/cnc/itc/datareadiness/enums/CompletenessCategory.java`

```java
package com.vertex.cnc.itc.datareadiness.enums;

import lombok.Getter;

@Getter
public enum CompletenessCategory {
    BASIS("Basis"),
    TAX("Tax");

    CompletenessCategory(String category)  { this.category = category; }
    private String category;

}

```

