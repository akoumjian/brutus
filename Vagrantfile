Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  ## Synced folders
  config.vm.synced_folder ".", "/opt/brutus"

  config.vm.provider :virtualbox do |v|
    v.memory = 4000
    v.cpus = 2
    v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
  end

end
