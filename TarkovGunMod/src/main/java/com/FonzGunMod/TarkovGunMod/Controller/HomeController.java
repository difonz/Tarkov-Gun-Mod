package com.FonzGunMod.TarkovGunMod.Controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
    public class HomeController {
        @GetMapping("/Index")
        public String Home(@RequestParam(name="name", required = false,defaultValue = "Welcome")String Name, Model model)
        {
            model.addAttribute("name", Name);
            return "Home";
        }
}

