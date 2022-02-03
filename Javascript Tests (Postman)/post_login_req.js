var jsonData = JSON.parse(responseBody);

tests["Access token was not empty"] = jsonData.access_token !== undefined;

postman.setEnvironmentVariable("jwt_token", jsonData.access_token);
