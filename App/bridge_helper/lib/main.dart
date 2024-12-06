// import 'package:mongo_dart/mongo_dart.dart' as mongo;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'dart:io';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const MyHomePage(),
        '/second': (context) => const BiddingPage(),
      },
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class BiddingPage extends StatefulWidget {
  const BiddingPage({super.key});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  @override
  State<BiddingPage> createState() => _Bidding();
}

class _Bidding extends State<BiddingPage> {
  List<List<String>> tableData = [
    ['Pass', 'Pass', 'Pass', '1NT'],
    ['Pass', '2♥️', 'Pass', '2♠️'],
    ['Pass', '4♠️', 'Pass', 'Pass'],
    ['Pass', '', '', '']
  ];

  bool showNewButtons = false;

  void _showNewButtons() {
    setState(() {
      showNewButtons = true;
    });
  }

  void _showOriginalButtons() {
    setState(() {
      showNewButtons = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            Flexible(
              flex: 5,
              child: Column(
                children: [
                  // Column Titles
                  Center(
                    child: Table(
                      columnWidths: const {
                        0: FlexColumnWidth(),
                        1: FlexColumnWidth(),
                        2: FlexColumnWidth(),
                        3: FlexColumnWidth(),
                      },
                      children: const [
                        TableRow(
                          children: [
                            Center(
                                child: Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Text.rich(
                                TextSpan(
                                  children: [
                                    TextSpan(
                                        text: 'West',
                                        style: TextStyle(color: Colors.red))
                                  ],
                                ),
                              ),
                            )),
                            Center(
                              child: Padding(
                                padding: const EdgeInsets.all(8.0),
                                child: Text.rich(
                                  TextSpan(
                                    children: [
                                      TextSpan(
                                          text: 'North',
                                          style: TextStyle(color: Colors.black))
                                    ],
                                  ),
                                ),
                              ),
                            ),
                            Center(
                                child: Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Text.rich(
                                TextSpan(
                                  children: [
                                    TextSpan(
                                        text: 'East',
                                        style: TextStyle(color: Colors.red))
                                  ],
                                ),
                              ),
                            )),
                            Center(
                                child: Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Text.rich(
                                TextSpan(
                                  children: [
                                    TextSpan(
                                        text: 'South',
                                        style: TextStyle(color: Colors.black))
                                  ],
                                ),
                              ),
                            )),
                          ],
                        ),
                      ],
                    ),
                  ),
                  Expanded(
                    child: SingleChildScrollView(
                      child: Center(
                        child: Column(
                          children: tableData.map((rowData) {
                            return DataRowWidget(rowData: rowData);
                          }).toList(),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const Spacer(flex: 1),
            const Text("♠️: Q84, ♥️: AK, ♦️: A96 ,♣️: QJT98",
                style: TextStyle(fontSize: 30)),
            const Spacer(flex: 1),
            Flexible(
                flex: 3,
                child: Column(children: [
                  if (showNewButtons)
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: <Widget>[
                        IconButton(
                          icon: Icon(Icons.arrow_back),
                          onPressed: _showOriginalButtons,
                        ),
                        ElevatedButton(
                          onPressed: () {
                            ///// Action for new button 5
                          },
                          child: Text('NT'),
                        ),
                        ElevatedButton(
                          onPressed: () {
                            // Action for new button 1
                          },
                          child: Text('♠️'),
                        ),
                        ElevatedButton(
                          onPressed: () {
                            //// Action for new button 2
                          },
                          child: Text('♥️'),
                        ),
                        ElevatedButton(
                          onPressed: () {
                            ///// Action for new button 3
                          },
                          child: Text('♦️'),
                        ),
                        ElevatedButton(
                          onPressed: () {
                            ///// Action for new button 4
                          },
                          child: Text('♣️'),
                        ),
                      ],
                    )
                  else
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: <Widget>[
                        ElevatedButton(
                          onPressed: _showNewButtons,
                          child: Text('1'),
                        ),
                        ElevatedButton(
                          onPressed: _showNewButtons,
                          child: Text('2'),
                        ),
                        ElevatedButton(
                          onPressed: _showNewButtons,
                          child: Text('3'),
                        ),
                        ElevatedButton(
                          onPressed: _showNewButtons,
                          child: Text('4'),
                        ),
                        ElevatedButton(
                          onPressed: _showNewButtons,
                          child: Text('5'),
                        ),
                        ElevatedButton(
                          onPressed: _showNewButtons,
                          child: Text('6'),
                        ),
                        ElevatedButton(
                          onPressed: _showNewButtons,
                          child: Text('7'),
                        ),
                      ],
                    ),
                ])),
            const Spacer(),
          ],
        ),
      ),
    );
  }
}

class _MyHomePageState extends State<MyHomePage> {
  static int _counter = 2;
  static const int _cap = 10;
  int _diff = _cap - _counter;

  void closeAppUsingSystemPop() {
    SystemChannels.platform.invokeMethod('SystemNavigator.pop');
  }

  void _goToEnterScores() {
    Navigator.pushNamed(context, '/second');
  }

  void _incrementCounter() {
    setState(() {
      // This call to setState tells the Flutter framework that something has
      // changed in this State, which causes it to rerun the build method below
      // so that the display can reflect the updated values. If we changed
      // _counter without calling setState(), then the build method would not be
      // called again, and so nothing would appear to happen.
      _counter++;
      _diff = _cap - _counter;
      if (_diff <= 0) {
        closeAppUsingSystemPop();
        exit(0);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // TRY THIS: Try changing the color here to a specific color (to
        // Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
        // change color while the other colors stay the same.
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.

        child: Column(
          // Column is also a layout widget. It takes a list of children and
          // arranges them vertically. By default, it sizes itself to fit its
          // children horizontally, and tries to be as tall as its parent.
          //
          // Column has various properties to control how it sizes itself and
          // how it positions its children. Here we use mainAxisAlignment to
          // center the children vertically; the main axis here is the vertical
          // axis because Columns are vertical (the cross axis would be
          // horizontal).
          //
          // TRY THIS: Invoke "debug painting" (choose the "Toggle Debug Paint"
          // action in the IDE, or press "p" in the console), to see the
          // wireframe for each widget.
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            Text('If you press it $_diff more times, the program will stop.'),
            FloatingActionButton(
              onPressed: _incrementCounter,
              tooltip: 'Increment',
              child: const Icon(Icons.add),
            ),
            ElevatedButton(
              onPressed: _goToEnterScores,
              child: const Icon(Icons.score_sharp),
            ),
          ],
        ),
      ),
      // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}

class DataRowWidget extends StatelessWidget {
  final List<String> rowData;
  DataRowWidget({required this.rowData});
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 1.0),
      child: Table(
        columnWidths: const {
          0: FlexColumnWidth(),
          1: FlexColumnWidth(),
          2: FlexColumnWidth(),
          3: FlexColumnWidth(),
        },
        children: [
          TableRow(
            children: rowData.map((cellData) {
              return Center(
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    cellData,
                    style: TextStyle(
                      fontSize: 14.0,
                      // Adjust the size to make the text smaller
                    ),
                  ),
                ),
              );
            }).toList(),
          )
        ],
      ),
    );
  }
}
