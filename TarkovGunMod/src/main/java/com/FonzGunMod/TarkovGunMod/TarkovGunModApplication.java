package com.FonzGunMod.TarkovGunMod;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import java.io.File;
import java.util.concurrent.ExecutionException;

@SpringBootApplication
public class TarkovGunModApplication {

	public static void main(String[] args) {

		SpringApplication.run(TarkovGunModApplication.class, args);
		// Runs python file to create the CSV files
		try {
			System.out.println("Retrieving Data.....");
			Process process =Runtime.getRuntime().exec("C:\\\\Python\\\\python.exe \\Data\\WeaponDatasheet.py");
			Process process2=Runtime.getRuntime().exec("C:\\\\Python\\\\python.exe \\Data\\GunModDatasheet.py");

			System.out.println("Data Retrieved.");
		}catch (Exception ex){
			ex.printStackTrace();
		}
	}

}
