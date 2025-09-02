package com.example.app_paciente.api

import com.example.app_paciente.model.UserRegisterRequest
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface ApiService {
    @POST("api/register/")
    fun registerUser(@Body user: UserRegisterRequest): Call<Map<String, String>>
}
