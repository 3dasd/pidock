FROM scratch

USER root
ADD root.tar /
RUN apt-get update && \
    apt-get install -y \
        vim tmux wiringpi \
        python3-pip libffi-dev libssl-dev

# Enable pubkey auth only
RUN sed -i 's/#PubkeyAuthentication.*/PubkeyAuthentication yes/g' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication.*/PasswordAuthentication no/g' /etc/ssh/sshd_config

# Install Platformio
RUN sudo -u pi python3 -c "$(curl -fsSL https://raw.githubusercontent.com/platformio/platformio/master/scripts/get-platformio.py)"
# Need this because of https://community.platformio.org/t/pio-broke-down-on-my-raspberry-pi-4/15819/2
RUN sudo -u pi /home/pi/.platformio/penv/bin/pio update
# This will fail but that's okay, we're only doing this to download
# every dependency of the remote agent.
RUN sudo -u pi /home/pi/.platformio/penv/bin/pio remote agent
# Add `pio` to the path
RUN echo 'export PATH=$PATH:/home/pi/.platformio/penv/bin' >> /home/pi/.bashrc
# HACK: Remote upload fails without this...
RUN ln -s /home/pi/.platformio/penv/bin/platformio /bin/platformio

# Enable access to serial port
RUN usermod -a -G dialout pi

# Copy everything from root-overlay/
ADD root-overlay /
RUN chown -R pi:pi /home/pi
 
# Manual steps required:
# - enable wifi
# - add SSH pub key in /home/pi/.ssh/authorized_keys
# - enable serial (but NOT login via serial) with raspi-config
# - edit /etc/systemd/system/pio-remote.service to add token
# - sudo systemctl enable pio-remote && sudo systemctl start pio-remote
# - 