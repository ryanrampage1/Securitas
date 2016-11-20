# Securitas

Securitas is a Python library for integrating Symantec VIP two factor authentication into any application.

## Installation

< Temporary, could be wrong, need to test! >

Install:

    $ pip install securitas

## Obtaining a certificate

To use Securitas in your project you first need a certificate from [Symantec VIP manager](https://manager.vip.symantec.com).
To obtain a certificate login and go to Account -> Manage VIP Certificates -> Request a Certificate. From there follow
the directions to create a new certificate. On the download screen select the PKCS#12 format and enter the password you
would like to use to secure the certificate.

After downloading the PKCS#12 certificate, you must split it into a public and private key. To do so run the following two
commands.

Extract the private key:

    $ openssl pkcs12 -in yourP12File.pfx -nocerts -out privateKey.pem

Extract the public certificate:

    $ openssl pkcs12 -in yourP12File.pfx -clcerts -nokeys -out publicCert.pem

## Usage

Once the certificate is split, Securitas is simple to start using.

< Insert Python instruction >

## Documentation

< Need to provide link once published! >

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/ryanrampage1/Securitas. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct.
