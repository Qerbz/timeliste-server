package com.falkbit.EMS.organization;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Data
public class Organization {
    @Id
    @SequenceGenerator(
            name = "organization_id_sequence",
            sequenceName = "organization_id_sequence"
    )
    @GeneratedValue(
            strategy = GenerationType.SEQUENCE,
            generator = "organization_id_sequence"
    )
    private Integer id;
    private String name;
}