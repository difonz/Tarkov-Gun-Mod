package com.FonzGunMod.TarkovGunMod.Repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.FonzGunMod.TarkovGunMod.Model.Weapons;

public interface WeaponsRepository extends JpaRepository<Weapons,Long>
{

}
