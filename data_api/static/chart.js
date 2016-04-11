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

		$.plot("#placeholder", data, options);

		// Fetch one series, adding to what we already have

		var alreadyFetched = {};

		$(function () {

			data = [];
			alreadyFetched = {};

			$.plot("#placeholder", data, options);

			var iteration = 0;

			function fetchData() {

				++iteration;

				function onDataReceived(series) {
					data.push([iteration, series.last]);
                    
					$.plot("#placeholder", [data], options);
				}

				$.ajax({
					url: "/last/{{symbol}}",
					type: "GET",
					dataType: "json",
					success: onDataReceived
				});
				
				if ( iteration < 50) {
					setTimeout(fetchData, 500);
				    }
			}

			setTimeout(fetchData, 1000);
		});

		$("button.fetchSeries:first").click();

		//$("#footer").prepend("Flot " + $.plot.version + " &ndash; ");
	});
