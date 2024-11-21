import 'package:app/pages/home_page.dart';
import 'package:app/pages/login_page.dart';
import 'package:app/pages/register_page.dart';
import 'package:app/pages/splash_page.dart';
import 'package:app/utils/theme.dart';
import 'package:flutter/material.dart';

/// The Widget that configures your application.
class htn2024 extends StatelessWidget {
  const htn2024({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      restorationScopeId: 'htn2024',
      theme: theme,
      initialRoute: SplashPage.routeName,
      routes: {
        SplashPage.routeName: (context) => const SplashPage(),
        LoginPage.routeName: (context) => const LoginPage(),
        RegisterPage.routeName: (context) => const RegisterPage(),
        HomePage.routeName: (context) => const HomePage(),
      },
    );
  }
}
