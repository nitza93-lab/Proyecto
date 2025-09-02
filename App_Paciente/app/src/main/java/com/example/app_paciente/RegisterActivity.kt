package com.example.app_paciente

import android.os.Bundle
import android.util.Log
import android.view.MotionEvent
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import com.example.app_paciente.api.RetrofitClient
import com.example.app_paciente.model.UserRegisterRequest
import android.text.method.PasswordTransformationMethod
import android.text.method.HideReturnsTransformationMethod

class RegisterActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.register)

        val etFirstName = findViewById<EditText>(R.id.editTextText_name)
        val etUsername = findViewById<EditText>(R.id.editText_user)
        val etEmail = findViewById<EditText>(R.id.editText_email)

        etEmail.setOnFocusChangeListener { _, hasFocus ->
            if (hasFocus && etEmail.text.toString() == "Correo electrónico") {
                etEmail.text.clear()
            }
        }

        val etPassword = findViewById<EditText>(R.id.editText_pass)
        val etPassword2 = findViewById<EditText>(R.id.editText_pass2)
        val btnRegister = findViewById<Button>(R.id.button_register)

        // Flag para visibilidad
        var isPasswordVisible = false

        etPassword.setOnTouchListener { v, event ->
            val DRAWABLE_END = 2
            if (event.action == MotionEvent.ACTION_UP &&
                event.x >= (etPassword.right - etPassword.compoundDrawables[DRAWABLE_END].bounds.width())
            ) {
                isPasswordVisible = !isPasswordVisible

                if (isPasswordVisible) {
                    etPassword.transformationMethod = HideReturnsTransformationMethod.getInstance()
                    etPassword.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.drawable.ic_eye_off, 0)
                } else {
                    etPassword.transformationMethod = PasswordTransformationMethod.getInstance()
                    etPassword.setCompoundDrawablesWithIntrinsicBounds(0, 0, R.drawable.ic_eye, 0)
                }

                // Mover cursor solo si hay texto
                etPassword.text?.let {
                    if (it.isNotEmpty()) etPassword.setSelection(it.length)
                }

                true
            } else {
                false
            }
        }



        btnRegister.setOnClickListener {

            Log.d("RegistryDebug", "Botón de registro presionado")  // <-- este log
            Toast.makeText(this, "Presionaste el botón", Toast.LENGTH_SHORT).show()
            val user = UserRegisterRequest(
                first_name = etFirstName.text.toString(),
                username = etUsername.text.toString(),
                email = etEmail.text.toString(),
                password = etPassword.text.toString()
            )

            RetrofitClient.api.registerUser(user).enqueue(object : Callback<Map<String, String>> {
                override fun onResponse(call: Call<Map<String, String>>, response: Response<Map<String, String>>) {
                    if (response.isSuccessful) {
                        Toast.makeText(this@RegisterActivity, "✅ Registro exitoso", Toast.LENGTH_SHORT).show()

                        // Limpiar campos
                        etFirstName.text.clear()
                        etUsername.text.clear()
                        etEmail.text.clear()
                        etPassword.text.clear()
                        etPassword2.text.clear()

                    } else {
                        // Imprime el error del servidor en Logcat
                        val errorBody = response.errorBody()?.string()
                        Log.e("RegistroError", "❌ Error en el registro: $errorBody")
                        Toast.makeText(this@RegisterActivity, "❌ Registro fallido", Toast.LENGTH_SHORT).show()
                    }
                }

                override fun onFailure(call: Call<Map<String, String>>, t: Throwable) {
                    Log.e("RegistroError", "❌ Fallo en la petición: ${t.message}")
                    Toast.makeText(this@RegisterActivity, "⚠ Error: ${t.message}", Toast.LENGTH_SHORT).show()
                }
            })

        }
    }
}
