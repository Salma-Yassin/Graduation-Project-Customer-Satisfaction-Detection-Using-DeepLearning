/*

=========================================================
* Volt Pro - Premium Bootstrap 5 Dashboard
=========================================================

* Product Page: https://themesberg.com/product/admin-dashboard/volt-bootstrap-5-dashboard
* Copyright 2021 Themesberg (https://www.themesberg.com)

* Designed and coded by https://themesberg.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. Please contact us to request a removal. Contact us if you want to remove it.

*/

"use strict";
const d = document;

d.addEventListener("DOMContentLoaded", function (event) {

    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-primary me-3',
            cancelButton: 'btn btn-gray'
        },
        buttonsStyling: false
    });

    var themeSettingsEl = document.getElementById('theme-settings');
    var themeSettingsExpandEl = document.getElementById('theme-settings-expand');

    if (themeSettingsEl) {

        var themeSettingsCollapse = new bootstrap.Collapse(themeSettingsEl, {
            show: true,
            toggle: false
        });

        if (window.localStorage.getItem('settings_expanded') === 'true') {
            themeSettingsCollapse.show();
            themeSettingsExpandEl.classList.remove('show');
        } else {
            themeSettingsCollapse.hide();
            themeSettingsExpandEl.classList.add('show');
        }

        themeSettingsEl.addEventListener('hidden.bs.collapse', function () {
            themeSettingsExpandEl.classList.add('show');
            window.localStorage.setItem('settings_expanded', false);
        });

        themeSettingsExpandEl.addEventListener('click', function () {
            themeSettingsExpandEl.classList.remove('show');
            window.localStorage.setItem('settings_expanded', true);
            setTimeout(function () {
                themeSettingsCollapse.show();
            }, 300);
        });
    }

    // options
    const breakpoints = {
        sm: 540,
        md: 720,
        lg: 960,
        xl: 1140
    };

    var sidebar = document.getElementById('sidebarMenu')
    if (sidebar && d.body.clientWidth < breakpoints.lg) {
        sidebar.addEventListener('shown.bs.collapse', function () {
            document.querySelector('body').style.position = 'fixed';
        });
        sidebar.addEventListener('hidden.bs.collapse', function () {
            document.querySelector('body').style.position = 'relative';
        });
    }

    var iconNotifications = d.querySelector('.notification-bell');
    if (iconNotifications) {
        iconNotifications.addEventListener('shown.bs.dropdown', function () {
            iconNotifications.classList.remove('unread');
        });
    }

    [].slice.call(d.querySelectorAll('[data-background]')).map(function (el) {
        el.style.background = 'url(' + el.getAttribute('data-background') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-background-lg]')).map(function (el) {
        if (document.body.clientWidth > breakpoints.lg) {
            el.style.background = 'url(' + el.getAttribute('data-background-lg') + ')';
        }
    });

    [].slice.call(d.querySelectorAll('[data-background-color]')).map(function (el) {
        el.style.background = 'url(' + el.getAttribute('data-background-color') + ')';
    });

    [].slice.call(d.querySelectorAll('[data-color]')).map(function (el) {
        el.style.color = 'url(' + el.getAttribute('data-color') + ')';
    });

    //Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })


    // Popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })


    // Datepicker
    var datepickers = [].slice.call(d.querySelectorAll('[data-datepicker]'))
    var datepickersList = datepickers.map(function (el) {
        return new Datepicker(el, {
            buttonClass: 'btn'
        });
    })

    if (d.querySelector('.input-slider-container')) {
        [].slice.call(d.querySelectorAll('.input-slider-container')).map(function (el) {
            var slider = el.querySelector(':scope .input-slider');
            var sliderId = slider.getAttribute('id');
            var minValue = slider.getAttribute('data-range-value-min');
            var maxValue = slider.getAttribute('data-range-value-max');

            var sliderValue = el.querySelector(':scope .range-slider-value');
            var sliderValueId = sliderValue.getAttribute('id');
            var startValue = sliderValue.getAttribute('data-range-value-low');

            var c = d.getElementById(sliderId),
                id = d.getElementById(sliderValueId);

            noUiSlider.create(c, {
                start: [parseInt(startValue)],
                connect: [true, false],
                //step: 1000,
                range: {
                    'min': [parseInt(minValue)],
                    'max': [parseInt(maxValue)]
                }
            });
        });
    }

    if (d.getElementById('input-slider-range')) {
        var c = d.getElementById("input-slider-range"),
            low = d.getElementById("input-slider-range-value-low"),
            e = d.getElementById("input-slider-range-value-high"),
            f = [d, e];

        noUiSlider.create(c, {
            start: [parseInt(low.getAttribute('data-range-value-low')), parseInt(e.getAttribute('data-range-value-high'))],
            connect: !0,
            tooltips: true,
            range: {
                min: parseInt(c.getAttribute('data-range-value-min')),
                max: parseInt(c.getAttribute('data-range-value-max'))
            }
        }), c.noUiSlider.on("update", function (a, b) {
            f[b].textContent = a[b]
        });
    }

    var getLocationData = $.get('/empolyee_data');
    getLocationData.done(function (empolyees) {
        if (d.querySelector('#empolyee_id_data')) {
            console.log(empolyees);
            const select = d.getElementById('empolyee_id_data');

            empolyees.forEach(option => {
                const optionElem = d.createElement('option');
                optionElem.value = option.member_id;
                optionElem.text = option.member_id;
                select.appendChild(optionElem);
            });

        }
    })

    var getLocationData = $.get('/location_data');
    getLocationData.done(function (locations) {
        if (d.querySelector('#empolyee_location')) {
            console.log(locations);
            const select = d.getElementById('empolyee_location');

            locations.forEach(option => {
                const optionElem = d.createElement('option');
                optionElem.value = option.name;
                optionElem.text = option.name;
                select.appendChild(optionElem);
            });

        }
    })


    var detailed_data = 'ay 7agaaa';
    var getMediaData = $.get('/media_data');

    getMediaData.done(function (results) {
        if (d.querySelector('#example')) {
            console.log(results);
            var table = jQuery('#example').DataTable({
                data: results,
                scrollX: false,
                columns: [
                    { data: 'id', title: '<b>ID</b>' },
                    { data: 'type' },
                    {
                        data: 'results',
                        render: function (data) {
                            if (data === 'Satisfied') {
                                return '<span class="badge bg-success fs-6">' + data + '</span>';
                            } else if (data === 'Unsatisfied') {
                                return '<span class="badge bg-danger fs-6">' + data + '</span>';
                            } else {
                                return '<span class="badge bg-warning fs-6">' + data + '</span>';
                            }
                        }
                    },
                    { data: 'member_id' },
                    { data: 'location_address' },
                    /*{
                        data: 'url',
                        render: function (data) {
                            return '<a href="' + data + '" target="_blank">' + data + '</a>';
                        }
                    },*/
                    { data: 'media_name' },
                    {
                        data: null,
                        className: 'details-control',
                        defaultContent: '<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal" data-bs-whatever="@mdo"><svg class="icon icon-xs me-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>Details</button>',
                        orderable: false
                    }
                ],
                columnDefs: [
                    {
                        targets: 5, // url column
                        width: '20%'
                    }
                ],

                initComplete: function () {
                    this.api()
                        .columns()
                        .every(function () {
                            var column = this;
                            if (!column.nodes().to$().hasClass('details-control')) {
                                var select = $('<select><option value=""></option></select>')
                                    .appendTo($(column.footer()).empty())
                                    .on('change', function () {
                                        var val = $.fn.dataTable.util.escapeRegex($(this).val());

                                        column.search(val ? '^' + val + '$' : '', true, false).draw();
                                    });

                                column
                                    .data()
                                    .unique()
                                    .sort()
                                    .each(function (d, j) {
                                        select.append('<option value="' + d + '">' + d + '</option>');
                                    });
                            }
                        });
                }
            });

            $('#example tbody').on('click', 'button', function () {
                var data = table.row($(this).parents('tr')).data();
                detailed_data = data.detailed_results
                //detailed_data = $.parseJSON(data.detailed_results);
                //console.log(detailed_data);

                //localStorage.setItem("passing_data", detailed_data);
                // console.log(data.type);
                // var scores=[];
                // var labels=[];
                //detailed_data.forEach(({score}) => scores.push(score));
                //console.log(scores)
                //detailed_data.forEach(({label}) => console.log(label));

                if (data.type === 'Video') {
                    // Do something for videos
                    console.log('Video clicked');
                    $.ajax({
                        type: 'POST',
                        url: '/update_chart_raw',
                        data: JSON.stringify(data.detailed_results),
                        contentType: 'application/json',
                        success: function (response) {
                            console.log(response);
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });
                    // Navigate to another view
                    window.location.href = '/pages/MediaAnalysis/';
                } else if (data.type === 'Audio') {
                    // Do something for audio
                    console.log('Audio clicked');
                    $.ajax({
                        type: 'POST',
                        url: '/update_chart_raw',
                        data: JSON.stringify(data.detailed_results),
                        contentType: 'application/json',
                        success: function (response) {
                            console.log(response);
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });
                    $.ajax({
                        type: 'POST',
                        url: '/play_media',
                        data: JSON.stringify(data.url),
                        contentType: 'application/json',
                        success: function (response) {
                            console.log(response);
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });
                    // Navigate to another view
                    window.location.href = '/pages/MediaAnalysisAudio/';
                } else {
                    // Do something else
                    console.log('Unknown type clicked');
                }
            });
        }
        console.log(checkvar);
    });


    var getplayMedia = $.get('/play_media');
    getplayMedia.done(function (results) {
        console.log(results)
        const audioPlay = d.getElementById("play-audio");
        audioPlay.src = results;

    })

    //Donught Chart:

    console.log(detailed_data);
    var getchartRaw = $.get('/update_chart_raw');
    getchartRaw.done(function (results) {
        results = $.parseJSON(results);

        if (d.querySelector(".ct-chart-audio")) {
            //results = $.parseJSON(results);
            console.log(results)

            var scores = [];
            var labels = [];
            results.forEach(({ score }) => scores.push((score * 100).toFixed(2)));
            results.forEach(({ label }) => labels.push(label));
            console.log(scores)

            var chart = new Chartist.Pie('.ct-chart-audio', {
                series: scores,
                labels: scores
            }, {
                donut: true,
                donutWidth: 80,
                startAngle: 0,
                showLabel: true
                //labelOffset: 40,
            });

            chart.on('draw', function (data) {
                if (data.type === 'slice') {
                    // Get the total path length in order to use for dash array animation
                    var pathLength = data.element._node.getTotalLength();

                    // Set a dasharray that matches the path length as prerequisite to animate dashoffset
                    data.element.attr({
                        'stroke-dasharray': pathLength + 'px ' + pathLength + 'px'
                    });

                    // Create animation definition while also assigning an ID to the animation for later sync usage
                    var animationDefinition = {
                        'stroke-dashoffset': {
                            id: 'anim' + data.index,
                            dur: 1000,
                            from: -pathLength + 'px',
                            to: '0px',
                            easing: Chartist.Svg.Easing.easeOutQuint,
                            // We need to use `fill: 'freeze'` otherwise our animation will fall back to initial (not visible)
                            fill: 'freeze'
                        }
                    };

                    // If this was not the first slice, we need to time the animation so that it uses the end sync event of the previous animation
                    if (data.index !== 0) {
                        animationDefinition['stroke-dashoffset'].begin = 'anim' + (data.index - 1) + '.end';
                    }

                    // We need to set an initial value before the animation starts as we are not in guided mode which would do that for us
                    data.element.attr({
                        'stroke-dashoffset': -pathLength + 'px'
                    });

                    // We can't use guided mode as the animations need to rely on setting begin manually
                    // See http://gionkunz.github.io/chartist-js/api-documentation.html#chartistsvg-function-animate
                    data.element.animate(animationDefinition, false);
                }
            });

            // For the sake of the example we update the chart every time it's created with a delay of 8 seconds
            chart.on('created', function () {
                if (window.__anim21278907124) {
                    clearTimeout(window.__anim21278907124);
                    window.__anim21278907124 = null;
                }
                window.__anim21278907124 = setTimeout(chart.update.bind(chart), 10000);
            });

        }
        if (d.querySelector(".ct-chart-body")) {
            /// will be changed:
            /*results = $.parseJSON(results);
            console.log(results)

            var scores = [];
            var labels = [];
            results.forEach(({ score }) => scores.push(score));
            results.forEach(({ label }) => labels.push(label));
            console.log(scores)*/
            var chart = new Chartist.Pie('.ct-chart-body', {
                series: [10, 70, 50, 20],
                labels: ['10%', '70%', '50%', '20%']
            }, {
                donut: true,
                donutWidth: 80,
                startAngle: 0,
                showLabel: true
            });

            chart.on('draw', function (data) {
                if (data.type === 'slice') {
                    // Get the total path length in order to use for dash array animation
                    var pathLength = data.element._node.getTotalLength();

                    // Set a dasharray that matches the path length as prerequisite to animate dashoffset
                    data.element.attr({
                        'stroke-dasharray': pathLength + 'px ' + pathLength + 'px'
                    });

                    // Create animation definition while also assigning an ID to the animation for later sync usage
                    var animationDefinition = {
                        'stroke-dashoffset': {
                            id: 'anim' + data.index,
                            dur: 1000,
                            from: -pathLength + 'px',
                            to: '0px',
                            easing: Chartist.Svg.Easing.easeOutQuint,
                            // We need to use `fill: 'freeze'` otherwise our animation will fall back to initial (not visible)
                            fill: 'freeze'
                        }
                    };

                    // If this was not the first slice, we need to time the animation so that it uses the end sync event of the previous animation
                    if (data.index !== 0) {
                        animationDefinition['stroke-dashoffset'].begin = 'anim' + (data.index - 1) + '.end';
                    }

                    // We need to set an initial value before the animation starts as we are not in guided mode which would do that for us
                    data.element.attr({
                        'stroke-dashoffset': -pathLength + 'px'
                    });

                    // We can't use guided mode as the animations need to rely on setting begin manually
                    // See http://gionkunz.github.io/chartist-js/api-documentation.html#chartistsvg-function-animate
                    data.element.animate(animationDefinition, false);
                }
            });

            // For the sake of the example we update the chart every time it's created with a delay of 8 seconds
            chart.on('created', function () {
                if (window.__anim21278907124) {
                    clearTimeout(window.__anim21278907124);
                    window.__anim21278907124 = null;
                }
                window.__anim21278907124 = setTimeout(chart.update.bind(chart), 10000);
            });

        }
        if (d.querySelector(".ct-chart-face")) {
            /// will be changed:
            /*results = $.parseJSON(results);
            console.log(results)

            var scores = [];
            var labels = [];
            results.forEach(({ score }) => scores.push(score));
            results.forEach(({ label }) => labels.push(label));
            console.log(scores)*/
            var value_chart_old = Object.values(results)
            var value_chart = []
            value_chart_old.forEach((item) => value_chart.push((item * 100).toFixed(2)));
            //value_chart=(value_chart*100).toFixed(2)
            var chart = new Chartist.Pie('.ct-chart-face', {
                series: value_chart,
                labels: value_chart
            }, {
                donut: true,
                donutWidth: 80,
                startAngle: 0,
                showLabel: true
            });

            chart.on('draw', function (data) {
                if (data.type === 'slice') {
                    // Get the total path length in order to use for dash array animation
                    var pathLength = data.element._node.getTotalLength();

                    // Set a dasharray that matches the path length as prerequisite to animate dashoffset
                    data.element.attr({
                        'stroke-dasharray': pathLength + 'px ' + pathLength + 'px'
                    });

                    // Create animation definition while also assigning an ID to the animation for later sync usage
                    var animationDefinition = {
                        'stroke-dashoffset': {
                            id: 'anim' + data.index,
                            dur: 1000,
                            from: -pathLength + 'px',
                            to: '0px',
                            easing: Chartist.Svg.Easing.easeOutQuint,
                            // We need to use `fill: 'freeze'` otherwise our animation will fall back to initial (not visible)
                            fill: 'freeze'
                        }
                    };

                    // If this was not the first slice, we need to time the animation so that it uses the end sync event of the previous animation
                    if (data.index !== 0) {
                        animationDefinition['stroke-dashoffset'].begin = 'anim' + (data.index - 1) + '.end';
                    }

                    // We need to set an initial value before the animation starts as we are not in guided mode which would do that for us
                    data.element.attr({
                        'stroke-dashoffset': -pathLength + 'px'
                    });

                    // We can't use guided mode as the animations need to rely on setting begin manually
                    // See http://gionkunz.github.io/chartist-js/api-documentation.html#chartistsvg-function-animate
                    data.element.animate(animationDefinition, false);
                }
            });

            // For the sake of the example we update the chart every time it's created with a delay of 8 seconds
            chart.on('created', function () {
                if (window.__anim21278907124) {
                    clearTimeout(window.__anim21278907124);
                    window.__anim21278907124 = null;
                }
                window.__anim21278907124 = setTimeout(chart.update.bind(chart), 10000);
            });

        }
    })





    //Chartist

    const handleChartData = (results) => {
        var cat = ['Unsatisfied', 'Neutral','Satisfied']
        var days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        var all = []
        for (let i = 0; i < cat.length; i++) {
            var series = []
            for (let j = 0; j < days.length; j++) {
                series = [...series, results.data.filter(row => ((row.results)).includes(cat[i])).filter(row => ((row.created_at)).includes(days[j])).length]
            }
            all = [...all, series]
        }
        return all
    }

    var getMedia_dummy_Data = $.get('/data');

    getMedia_dummy_Data.done(function (results) {

        var all = handleChartData(results)

        var all_satisfied = all[2];
        var all_unsatisfied = all[0];
        var all_neutral = all[1];

        const sum_satisfied = all_satisfied.reduce((total, current) => total + current, 0);
        const sum_unsatisifed = all_unsatisfied.reduce((total, current) => total + current, 0);
        const sum_neutral = all_neutral.reduce((total, current) => total + current, 0);
        const all_customers = sum_satisfied + sum_unsatisifed + sum_neutral
        var satisfied_per;
        if (all_customers==0) {
            satisfied_per = sum_satisfied*100/1;
        } else {
            satisfied_per = sum_satisfied*100/all_customers;
        }
        
        console.log(all_customers); // output: 15

        const textCustomers = d.getElementById("text-value-total-customers");
        textCustomers.textContent = all_customers;

        const textSatisifed = d.getElementById("text-value-total-satisfied");
        textSatisifed.textContent = sum_satisfied;

        const textUnSatisifed = d.getElementById("text-value-total-unsatisfied");
        textUnSatisifed.textContent = sum_unsatisifed;

        const textNeutral = d.getElementById("text-value-total-neutral");
        textNeutral.textContent = sum_neutral;

        const textSatisfiedPerc = d.getElementById("text-value-total-sat-percentage");
        textSatisfiedPerc.textContent = satisfied_per;


        console.log(all)

        if (d.querySelector('.ct-chart-ranking')) {

            //var series = results.data.filter(row =>((row.created_at)).includes('Fri')

            var chart = new Chartist.Bar('.ct-chart-ranking', {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                series: all
            }, {
                low: 0,
                showArea: true,
                plugins: [
                    Chartist.plugins.tooltip()
                ],
                axisX: {
                    // On the x-axis start means top and end means bottom
                    position: 'end'
                },
                axisY: {
                    // On the y-axis start means left and end means right
                    showGrid: false,
                    showLabel: false,
                    offset: 0
                }
            });

            chart.on('draw', function (data) {
                if (data.type === 'line' || data.type === 'area') {
                    data.element.animate({
                        d: {
                            begin: 2000 * data.index,
                            dur: 2000,
                            from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
                            to: data.path.clone().stringify(),
                            easing: Chartist.Svg.Easing.easeOutQuint
                        }
                    });
                }
            });
        }
        if (d.querySelector('.ct-chart-sales-value')) {
            //Chart 5
            new Chartist.Line('.ct-chart-sales-value', {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                series: all
            }, {
                low: 0,
                showArea: true,
                fullWidth: true,
                plugins: [
                    Chartist.plugins.tooltip()
                ],
                axisX: {
                    // On the x-axis start means top and end means bottom
                    position: 'end',
                    showGrid: true
                },
                axisY: {
                    // On the y-axis start means left and end means right
                    showGrid: false,
                    showLabel: false,
                    labelInterpolationFnc: function (value) {
                        return '$' + (value / 1) + 'k';
                    }
                }
            });
        }

    });


    if (d.querySelector('.ct-chart-traffic-share')) {
        var data = {
            series: [70, 20, 10]
        };

        var sum = function (a, b) { return a + b };

        new Chartist.Pie('.ct-chart-traffic-share', data, {
            labelInterpolationFnc: function (value) {
                return Math.round(value / data.series.reduce(sum) * 100) + '%';
            },
            low: 0,
            high: 8,
            donut: true,
            donutWidth: 50,
            donutSolid: true,
            fullWidth: false,
            showLabel: false,
            plugins: [
                Chartist.plugins.tooltip()
            ],
        });
    }

    if (d.getElementById('loadOnClick')) {
        d.getElementById('loadOnClick').addEventListener('click', function () {
            var button = this;
            var loadContent = d.getElementById('extraContent');
            var allLoaded = d.getElementById('allLoadedText');

            button.classList.add('btn-loading');
            button.setAttribute('disabled', 'true');

            setTimeout(function () {
                loadContent.style.display = 'block';
                button.style.display = 'none';
                allLoaded.style.display = 'block';
            }, 1500);
        });
    }

    var scroll = new SmoothScroll('a[href*="#"]', {
        speed: 500,
        speedAsDuration: true
    });

    if (d.querySelector('.current-year')) {
        d.querySelector('.current-year').textContent = new Date().getFullYear();
    }

    // Glide JS

    if (d.querySelector('.glide')) {
        new Glide('.glide', {
            type: 'carousel',
            startAt: 0,
            perView: 3
        }).mount();
    }

    if (d.querySelector('.glide-testimonials')) {
        new Glide('.glide-testimonials', {
            type: 'carousel',
            startAt: 0,
            perView: 1,
            autoplay: 2000
        }).mount();
    }

    if (d.querySelector('.glide-clients')) {
        new Glide('.glide-clients', {
            type: 'carousel',
            startAt: 0,
            perView: 5,
            autoplay: 2000
        }).mount();
    }

    if (d.querySelector('.glide-news-widget')) {
        new Glide('.glide-news-widget', {
            type: 'carousel',
            startAt: 0,
            perView: 1,
            autoplay: 2000
        }).mount();
    }

    if (d.querySelector('.glide-autoplay')) {
        new Glide('.glide-autoplay', {
            type: 'carousel',
            startAt: 0,
            perView: 3,
            autoplay: 2000
        }).mount();
    }

    // Pricing countup
    var billingSwitchEl = d.getElementById('billingSwitch');
    if (billingSwitchEl) {
        const countUpStandard = new countUp.CountUp('priceStandard', 99, { startVal: 199 });
        const countUpPremium = new countUp.CountUp('pricePremium', 199, { startVal: 299 });

        billingSwitchEl.addEventListener('change', function () {
            if (billingSwitch.checked) {
                countUpStandard.start();
                countUpPremium.start();
            } else {
                countUpStandard.reset();
                countUpPremium.reset();
            }
        });
    }




});