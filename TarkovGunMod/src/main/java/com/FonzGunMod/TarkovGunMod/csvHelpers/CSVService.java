package com.FonzGunMod.TarkovGunMod.csvHelpers;

import java.io.IOException;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.FonzGunMod.TarkovGunMod.csvHelpers.CSVHelper;
import com.FonzGunMod.TarkovGunMod.Model.Weapons;
import com.FonzGunMod.TarkovGunMod.Repository.WeaponsRepository;


@Service
public class CSVService {
    @Autowired
    WeaponsRepository repository;

    public void save(MultipartFile file) {
        try {
            List<Weapons> weapons = CSVHelper.csvToWeapons(file.getInputStream());
            repository.saveAll(weapons);
        } catch (IOException e) {
            throw new RuntimeException("fail to store csv data: " + e.getMessage());
        }
    }

    public List<Weapons> getAllWeapons() {
        return repository.findAll();
    }
}