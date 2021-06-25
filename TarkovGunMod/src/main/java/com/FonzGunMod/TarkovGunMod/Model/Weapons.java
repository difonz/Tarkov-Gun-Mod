package com.FonzGunMod.TarkovGunMod.Model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name="weapons")
public class Weapons{


    @Id
    @Column(name="id")
    private long Id;

    @Column(name="name")
    private String Name;

    @Column(name="Cartridge")
    private String Cartridge;

    @Column(name="Firing Modes")
    private String FireMode;

    @Column(name="Rate of Fire")
    private String RateOfFire;

    @Column(name="Description")
    private String Description;


    @Column(name="Image")
    private String Image;


    public Weapons(){}


    public Weapons(long Id, String Name, String Cartridge, String FireMode,String RateOfFire,String Description,String Image)
    {
        this.Id = Id;
        this.Cartridge = Cartridge;
        this.FireMode = FireMode;
        this.RateOfFire = RateOfFire;
        this.Description = Description;
        this.Image= Image;
    }
    public long getId() {
        return Id;
    }

    public String getName() {
        return Name;
    }

    public String getCartridge() {
        return Cartridge;
    }

    public String getFireMode() {
        return FireMode;
    }

    public String getRateOfFire() {
        return RateOfFire;
    }

    public String getDescription() {
        return Description;
    }

    public String getImage() {
        return Image;
    }

    @Override
    public String toString() {
        return "Weapons[" +
                "Id=" + Id +
                ", Name='" + Name + '\'' +
                ", Cartridge='" + Cartridge + '\'' +
                ", FireMode='" + FireMode + '\'' +
                ", RateOfFire='" + RateOfFire + '\'' +
                ", Description='" + Description + '\'' +
                ", Image='" + Image + '\'' +
                ']';
    }

}
