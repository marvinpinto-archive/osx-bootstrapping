# Yet another dotfile/package management framework?

Yep. My machine has been reformatted one too many times and because I hate
manually setting up things from scratch, here we are. This was also a good
opportunity to dig into Ansible as well and that's my excuse.

# My use cases

* Manage the bulk of my osx package installation & configuration
* Manage the installation of my dotfiles locally
* Manage the installation of my dotfiles remotely

The bulk of the servers I manage are only accessible through bastion hosts and
firewalled up the wazoo. They are usually blocked from accessing Internet hosts
like github, bitbucket so I needed a way to get my dotfiles on to them *and*
keeping them not-stale without having a `git pull` like mechanism.

This isn't perfect but it works for now.

# Is this useful for other people?

I don't know! It could be! My immediate goal was *getting this done* but if you
have ideas on improving this I would love to hear from you :)

# How does this even work?

#### Prerequisites

1. Install Xcode
  ```bash
  $ xcode-select --install
  ```
  (select the **Get Xcode** option and install the full suite)

1. Agree to the xcode license
  ```bash
  $ sudo xcrun cc
  ```

1. Install Homebrew
  ```bash
  $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  $ brew doctor
  ```

1. Install Ansible
  ```bash
  $ brew install ansible
  ```

1. Clone this repo locally
  ```bash
  $ git clone https://github.com/marvinpinto/osx-bootstrapping.git /tmp/osx-bootstrapping
  ```

#### Bootstrapping a fresh OSX system

Put the dotfiles in place locally using something like:
```bash
$ ansible-playbook \
  --diff \
  -v \
  --ask-vault-pass \
  -i /tmp/osx-bootstrapping/dotfiles/inventory \
  /tmp/osx-bootstrapping/dotfiles/osx.yml
```

Get all the osx applications & configuration in place using something like:
```bash
$ ansible-playbook \
  --diff \
  -v \
  --ask-vault-pass \
  --ask-sudo-pass \
  --extra-vars 'computername=<COMPUTER-NAME>' \
  --limit '<COMPUTER-NAME>' \
  -i /tmp/osx-bootstrapping/osx_apps/inventory /tmp/osx-bootstrapping/osx_apps/osx.yml
```

#### Installing dotfiles to a remote location

```bash
$ ansible-playbook \
  -v \
  --diff \
  --ask-vault-pass \
  --extra-vars "user=<USER> umask=<UMASK>" \
  -i <HOST>, \
  /tmp/osx-bootstrapping/dotfiles/servers.yml
```

Notice that snazzy comma `,` up there beside the `<SERVER>` entry? Essentially
got the idea from the StackOverflow question [How to run Ansible without specifying the inventory but the host directly][1]

> The host parameter preceding the , can be either a hostname or an IPv4
> address. It does not seem to work with IPv6 addresses though (not even with
> the [] notation).

[1]: http://stackoverflow.com/a/18255256/1101070

#### Testing

Sometimes you'll want to test things out on a vagrant image. Here's what I do:

```bash
$ ansible-playbook \
  -v \
  --diff \
  --ask-vault-pass \
  -i /tmp/osx-bootstrapping/dotfiles/inventory \
  /tmp/osx-bootstrapping/dotfiles/vagrant-test.yml
```

#### Day to day use

Seeing as I am never going to remember these verbose commands and knowing that
I'm going to be too lazy to look this up, I've made bash shorctuts to take care
of this for me:

* [dflocal][2]
* [dfosx][3]
* [dfremote][4]

[2]: ./dotfiles/roles/osx/files/aliases#L36
[3]: ./dotfiles/roles/osx/files/aliases#L39
[4]: ./dotfiles/roles/osx/files/functions#L3

# The manual things that make me sad

Like every great automation system, you're always left with a few interesting
things that need to be done manually. This is no exception.

I'm going to do my best to keep this list short but best intentions and all
that.

#### Manually install apps from the app store or elsewhere
* Microsoft Remote Desktop
* Netextender

#### Desktop background
* Change the desktop background to: `Solid Colors -> Solid Gray Dark`

#### System Avatar
* System Preferences -> Users & Groups -> User
* Drag and drog avatar.jpg onto that tiny image box.

#### Fix login items to ensure nothing other than the following are listed
* Dropbox
* Divvy

#### Configure Dropbox
* Do not show desktop notifications
* Start dropbox on system startup
* Enable Selective Sync
* Do not enable camera uploads
* Share screenshots using dropbox
* Enable LAN sync

#### Chrome Settings
Head over to [chrome://flags](http://chrome:flags) in Chrome and set the following:
* Disable Built-in Asynchronous DNS Client
* Disable experimental Synchronized Notifications

Then:

* Chrome Menu -> Hide notification icon
* Chrome Menu -> Warn Before Quitting (Cmd+Q)

#### Dock Icons
Ensure that the only application icons in the dock are:
* `chrome-new-window`
* `chrome-incognito`
* `iterm-new-window`

#### Enable accessibility for divvy
Reference [http://mizage.com/help/accessibility.html](http://mizage.com/help/accessibility.html)
* Security & Privacy (Privacy tab)
* Accessibility
* Check mark beside Divvy

#### Keyboard preferences
* Enable: adjust keyboard brightness in low light
* Turn keyboard brightness off when computer is not used for 5 seconds
* Modified Keys -> Change Caps lock to Ctrl
* Shortcuts -> Accessibility -> Map Cmd+Q to "Invert Colors"
