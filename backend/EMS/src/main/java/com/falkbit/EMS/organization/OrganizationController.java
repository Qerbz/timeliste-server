package com.falkbit.EMS.organization;

import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/organization")
public class OrganizationController {
    private final OrganizationDAO organizationDAO;

    public OrganizationController(OrganizationDAO organizationDAO) {
        this.organizationDAO = organizationDAO;
    }

    @GetMapping
    public List<Organization> getOrganizations(){
        List<Organization> organizationList = organizationDAO.findAll();
        System.out.println(Arrays.toString(organizationList.toArray()));
        return organizationList;
    }

    record NewOrganizationRequest(
            String name
    ){

    }

    @PostMapping
    public void addOrganization(@RequestBody NewOrganizationRequest request){
        Organization organization = new Organization();
        organization.setName(request.name());
        organizationDAO.save(organization);
    }

    @DeleteMapping("{organizationId}")
    public void deleteOrganization(@PathVariable("organizationId") Integer id){
        organizationDAO.deleteById(id);
    }
}
