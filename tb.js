function updateEstimator() {
        timenow = new Date();
        timenow_unix = new Date();
        timediff = Math.round((endtime_unix - timenow_unix) / 1000);
        timediff_pred = Math.round((endtime_pred - timenow_unix) / 1000);
        outputvalu = magicaway(timediff);
        outputvalu_pred = magicaway(timediff_pred);
//        document.getElementById('estimator').innerHTML = outputvalu;
//        document.getElementById('estimator_pred').innerHTML = outputvalu_pred;
	$('estimator').set('html', outputvalu);
	$('estimator_pred').set('html', outputvalu_pred);

	// now for estimator-end and estimator_pred end
	estimator_end = new Date();
	estimator_pred_end = new Date();

	estimator_end = estimator_end.increment('second', timediff);
	estimator_pred_end = estimator_pred_end.increment('second', timediff_pred);

	formatter = '(%x %X)';
	$('estimator-end').set('html', estimator_end.format(formatter));
	$('estimator_pred-end').set('html', estimator_pred_end.format(formatter));
}

function magicaway(timediff) {
        hourdiff = Math.floor(timediff / 60 / 60);
        timediff -= hourdiff * 60 * 60;

        mindiff = Math.floor(timediff / 60);
        timediff -= mindiff * 60;

        secdiff = timediff;

        if (mindiff < 10) {
                minpad = '0';
        } else {
                minpad = '';
        }
        if (secdiff < 10) {
                secpad = '0';
        } else {
                secpad = '';
        }
        return hourdiff + ':' + minpad + mindiff + ':' + secpad + secdiff;
}

JSONgrabber = new Request.JSON({url: '/data.json', onSuccess: function(newdata) {
	clearTimeout(saveb);
	$('potato-2').setStyle('width', newdata.logowidth);
	$('gamebar').set('html', newdata.gamebar);
	$('hoursahead').set('html', newdata.glados.ahead);
	$('hourspred').set('html', newdata.estimate.ahead);
	$('luclock').set('html', 'ajax-' + newdata.lastupdate);
	endtime = new Date();
	endtime_unix = endtime.getTime();
	endtime_pred = endtime_unix + Math.round(newdata.estimate.endpoint) * 1000;
	endtime_unix = endtime_unix + Math.round(newdata.glados.endpoint) * 1000;
	tooltip.init(); // reinit
        //$('more-info').set('html', pretext);
//        pretext = '';
}});
//pretext = '';
saveb = 0;
function updateEndpoint() {
  //  pretext = $('more-info').get('html');
//    $('more-info').set('html', 'Page updating...');
    saveb = setTimeout(forceRefresh, 10000);
    JSONgrabber.get();
}
function forceRefresh() {
    window.location = window.location;
}
ison = true;
function pulsate() {
        return false;
    faz = document.getElementsByClassName("current-focus");
    i = 0;
    if (ison == false) {
        ison = true;
        newopac = 1;
    } else {
        ison = false;
        newopac = 0.4;
    }
    while (i < faz.length) {
        fz = faz[i];
        fz.style.opacity = newopac;
        i = i + 1;
    }
}
function getDot() { return '.'; }
function getEnding() { return 'com'; }


//oldload = window.onload;
function newload() {
	em = document.getElementById('e3ma1l-a');
	em.onclick = function() {
	  a = document.getElementById('e3ma1l');
	  a.innerHTML = "hp2ly" + "@l" + "ukeg";
	  a.innerHTML = a.innerHTML + "b" + getDot() + getEnding();
	};
	setInterval("pulsate()", 500);
	setInterval('updateEndpoint()', 90000);
        setInterval('updateEstimator()', 40);
	// detect locale
	setl = Cookie.read('setlocale');
	if (setl == null) {
		Locale.AutoUse(navigator);
	} else {
		Locale.use(setl);
	}
	setl = Locale.getCurrent().name;
	// populate localebox
	$('localebox').empty();
	i = 0;
	ll = Locale.list();
	while (i < ll.length) {
		$('localebox').grab(new Element('option', {value: ll[i], html: ll[i]}));
		i = i + 1;
	}
	$('localebox').set('value', setl);
	$('localebox').addEvent('change', newlocale);
	$('locale-div').setStyle('visibility', 'visible');
}
//window.onload = newload;
window.addEvent('domready', newload);

function newlocale() {
	Cookie.write('setlocale', $(this).get('value'));
	Locale.use($(this).get('value'));
	// bing
}
