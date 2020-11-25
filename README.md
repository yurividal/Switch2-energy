# Switch2-energy
### Gets energy usage data from switch2.co.uk and stores it in influxDB

![Grafana Screenshot](/screenshot.png)
Grafana Dashboard with the data

## How to Use
- Install all necessary dependencies using pip
- Add your switch2.co.uk credentials and influxDB credentials to the script
- Choose if you want to grab all the data or just the latest measurement
- Run the script

Obs: If you just need the data and don't need to send it to influxDB, set ```write_to_influx = False```

## Credits
Special thanks to @skrobul and his project [Switch2Dump](https://github.com/skrobul/switch2dump) for the inspiration.
I simply adapted his project to use python instead of ruby and influxDB instead of postgre.
