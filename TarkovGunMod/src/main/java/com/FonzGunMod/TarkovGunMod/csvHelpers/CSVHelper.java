package com.FonzGunMod.TarkovGunMod.csvHelpers;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.web.multipart.MultipartFile;

import com.FonzGunMod.TarkovGunMod.Model.Weapons;


public class CSVHelper {
    public static String TYPE = "text/csv";
    static String[] HEADERS = {"Id", "Name", "Cartridge", "FiringModes", "RateOfFire", "Description", "Image"};

    public static boolean hasCSVFormat(MultipartFile file) {

        if (!TYPE.equals(file.getContentType())) {
            return false;
        }

        return true;
    }

    public static List<Weapons> csvToWeapons(InputStream is) {
        try (BufferedReader fileReader = new BufferedReader(new InputStreamReader(is, "UTF-8"));
             CSVParser csvParser = new CSVParser(fileReader,
                     CSVFormat.DEFAULT.withFirstRecordAsHeader().withIgnoreHeaderCase().withTrim());) {

            List<Weapons> weapons = new ArrayList<Weapons>();

            Iterable<CSVRecord> csvRecords = csvParser.getRecords();

            for (CSVRecord csvRecord : csvRecords) {
                Weapons weapon = new Weapons(

                        Long.parseLong(csvRecord.get("Id")),
                        csvRecord.get("name"),
                        csvRecord.get("Cartridge"),
                        csvRecord.get("FireMode"),
                        csvRecord.get("RateOfFire"),
                        csvRecord.get("Description"),
                        csvRecord.get("Image")
                );

                weapons.add(weapon);
            }

            return weapons;
        } catch (IOException e) {
            throw new RuntimeException("fail to parse CSV file: " + e.getMessage());
        }
    }

}