# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

    config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 2
    end

    config.vm.define "avmess" do |machine|
        machine.vm.box = "ubuntu/xenial64"

        machine.vm.network "private_network", ip: "192.168.10.55"

        machine.vm.synced_folder ".", "/opt/dev/avmess"

        config.vm.provision "shell", path: "./vagrant/provision.sh"
        config.vm.provision :shell, :inline => <<-EOT
            echo 'LC_ALL="en_US.UTF-8"'  >  /etc/default/locale
        EOT
    end
end
