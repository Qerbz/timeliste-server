package com.falkbit.EMS.Employee;

import com.falkbit.EMS.organization.Organization;
import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDate;

@Entity
@Data
public class Employee {
    @Id
    @SequenceGenerator(
            name = "employee_id_sequence",
            sequenceName = "employee_id_sequence"
    )
    @GeneratedValue(
            strategy = GenerationType.SEQUENCE,
            generator = "employee_id_sequence"
    )
    private Integer id;

    @ManyToOne
    @JoinColumn(name="organization_id", nullable = false)
    private Organization organization;
    private String firstName;
    private String lastName;
    private String email;
    private String phoneNumber;

//    @ManyToOne
//    @JoinColumn(name="position_id", nullable = false)
//    private Position position;
    private LocalDate HireDate;
    private Boolean isActive;
}
