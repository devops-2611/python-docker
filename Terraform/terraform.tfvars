vms = {
  vm01 = {
    rgname            = "student-rg"
    saname            = "studentsa"
    location          = "Canada central"
    vnname            = "kohlivn"
    address_space     = ["10.0.0.0/24"]
    snname            = "studentsn1"
    address_prefixes  = ["10.0.0.0/28"]
    piname            = "studentip"
    allocation_method = "Static"
    niname            = "studentnic"
    ipcname           = "studentipc"
    vmname            = "studentvm"
    size              = "Standard_F2"
  }
}