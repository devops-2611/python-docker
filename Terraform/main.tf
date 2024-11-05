variable "vms" {}
resource "azurerm_resource_group" "rgdodo" {
  name     = var.vms.vm01.rgname
  location = var.vms.vm01.location
}

resource "azurerm_storage_account" "sadodo" {
  name= var.vms.vm01.saname
  resource_group_name= var.vms.vm01.saname
  location            = var.vms.vm01.location
  account_tier= "Standard"
  account_replication_type = "LRS"
  
}
 resource "azurerm_storage_share" "shdodo" {
  name= "${var.vms.vm01.saname}-file-share"
  storage_account_name = var.vms.vm01.saname
  quota = 50
   
 }

resource "azurerm_virtual_network" "vndodo" {
  for_each            = var.vms
  name                = each.value.vnname
  location            = each.value.location
  resource_group_name = var.vms.vm01.rgname
  address_space       = each.value.address_space
  depends_on          = [azurerm_resource_group.rgdodo]
}
resource "azurerm_subnet" "sndodo" {
  for_each             = var.vms
  name                 = each.value.snname
  resource_group_name  = var.vms.vm01.rgname
  virtual_network_name = each.value.vnname
  address_prefixes     = each.value.address_prefixes
  depends_on           = [azurerm_virtual_network.vndodo]
}
resource "azurerm_public_ip" "pidodo" {
  for_each            = var.vms
  name                = each.value.piname
  resource_group_name = var.vms.vm01.rgname
  location            = each.value.location
  allocation_method   = each.value.allocation_method
  depends_on          = [azurerm_subnet.sndodo]
}
resource "azurerm_network_interface" "nidodo" {
  for_each            = var.vms
  name                = each.value.niname
  resource_group_name = var.vms.vm01.rgname
  location            = each.value.location
  depends_on          = [azurerm_public_ip.pidodo]
  ip_configuration {
    name                          = each.value.ipcname
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.pidodo[each.key].id
    subnet_id                     = azurerm_subnet.sndodo[each.key].id

  }
}


resource "azurerm_network_security_group" "nsgdodo" {
  for_each            = var.vms
  name                = "nsg_${each.key}"
  location            = each.value.location
  resource_group_name = var.vms.vm01.rgname
  depends_on          = [azurerm_resource_group.rgdodo]


}

resource "azurerm_network_security_rule" "http_3000_rule_vm01" {

  count                       = var.vms["vm01"] != null ? 1 : 0
  name                        = "allow-http-3000-vm01"
  priority                    = 103
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = var.vms.vm01.rgname
  network_security_group_name = azurerm_network_security_group.nsgdodo["vm01"].name
}






# Associate NSG with NIC using for_each
resource "azurerm_network_interface_security_group_association" "nsg_association" {
  for_each                  = var.vms
  network_interface_id      = azurerm_network_interface.nidodo[each.key].id
  network_security_group_id = azurerm_network_security_group.nsgdodo[each.key].id
  depends_on                = [azurerm_resource_group.rgdodo]
}



resource "azurerm_linux_virtual_machine" "vmdodo" {
  for_each                        = var.vms
  name                            = each.value.vmname
  resource_group_name             = var.vms.vm01.rgname
  location                        = each.value.location
  size                            = each.value.size
  disable_password_authentication = false
  admin_username                  = "dodouser"
  admin_password                  = "dodopassword@12345"
  network_interface_ids           = [azurerm_network_interface.nidodo[each.key].id]
  depends_on                      = [azurerm_network_interface.nidodo]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}


