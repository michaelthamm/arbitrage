<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <!--[if lte IE 8]><script language="javascript" type="text/javascript" src="../../excanvas.min.js"></script><![endif]-->
    <link href="{{ url('static', path='main.css') }}" rel="stylesheet" type="text/css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script type="text/javascript" src="{{ url('static', path='flot/jquery.flot.js') }}" charset="utf-8"></script>
    <script type="text/javascript">

	$(function() {

		var options = {
			lines: {
				show: true
			},
			points: {
				show: true
			},
			xaxis: {
				tickDecimals: 0,
				tickSize: 1
			}
		};

		var data = [];

		//$.plot("#placeholder", data, options);

		// Fetch one series, adding to what we already have

		var alreadyFetched = {};

		// Initiate a recurring data update

		//$("button.dataUpdate").click(function () {
		$(function () {

			data = [];
			alreadyFetched = {};

			$.plot("#placeholder", data, options);

			var iteration = 0;

			function fetchData() {

				++iteration;

				function onDataReceived(series) {
				    if (data.length>40){
    				data.shift();
    				}
					data.push([iteration, series.last]);
                    
					$.plot("#placeholder", [data], options);
				}

				$.ajax({
					url: "/last/{{symbol}}",
					type: "GET",
					dataType: "json",
					success: onDataReceived
				});
				
				if ( iteration < 100) {
					setTimeout(fetchData, 1000);
				    }
			}

			setTimeout(fetchData, 1000);
		});

		$("button.fetchSeries:first").click();

		//$("#footer").prepend("Flot " + $.plot.version + " &ndash; ");
	});

	</script>

	</script>
    <meta charset="UTF-8">
    <title>Chart for symbol: {{symbol}}</title>
  </head>
  <body>

	<div id="header">
		<h2>{{symbol}}</h2>
	</div>

	<div id="content">

		<div class="container">
			<div id="placeholder" class="placeholder"></div>
		</div>

		<p></p>

		<p></p>
        
        <p>
		</p>
	</div>

	<div id="footer">
	</div>

</body>
</html>
