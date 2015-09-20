# particlemap

Particle map based on the ELK stack

## setup

    pip install elasticsearch

Get the raw csv data

    wget --no-check-certificate -O rawdata/particledata.csv https://paste.madflex.de/d9rcQxUT/+inline


Start the container (see:  http://spujadas.github.io/elk-docker/#installation)

    sudo docker pull sebp/elk
    sudo docker run -p 5601:5601 -p 9200:9200 -p 5000:5000 -it --name particlebox sebp/elk

Import data
    
    python particle_import.py
    
Dashoard http://localhost:5601