from pathlib import Path

def replace_once(path, old, new, label):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match in {path}, found {count}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"Applied: {label}")

replace_once(
    "src/CMakeLists.txt",
    '''set(${PROJECT_NAME}_BRANCH_NAME "" CACHE STRING "name of the branch for self updates")

option(${PROJECT_NAME}_SELF_UPDATE "Enable the self-update feature")''',
    '''set(${PROJECT_NAME}_BRANCH_NAME "" CACHE STRING "name of the branch for self updates")

set(${PROJECT_NAME}_RELEASE_VERSION "development" CACHE STRING "version of this GitAddonsManager build")

option(${PROJECT_NAME}_SELF_UPDATE "Enable the self-update feature")''',
    "release version CMake setting",
)

replace_once(
    "src/CMakeLists.txt",
    '''add_compile_definitions(
    GIT_DESCRIBE="${${PROJECT_NAME}_GIT_DESCRIBE}"
    GAM_EXEC="GitAddonsManager${CMAKE_EXECUTABLE_SUFFIX}"
    )''',
    '''add_compile_definitions(
    GIT_DESCRIBE="${${PROJECT_NAME}_GIT_DESCRIBE}"
    GAM_EXEC="GitAddonsManager${CMAKE_EXECUTABLE_SUFFIX}"
    GAM_RELEASE_VERSION="${${PROJECT_NAME}_RELEASE_VERSION}"
    )''',
    "release version compile definition",
)

replace_once(
    "src/control.cpp",
    '''#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QApplication>''',
    '''#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QJsonDocument>
#include <QJsonArray>
#include <QJsonObject>
#include <QVersionNumber>
#include <QRegularExpression>
#include <QApplication>''',
    "update JSON/version includes",
)

replace_once(
    "src/control.cpp",
    '''Control *Control::m_instance = nullptr;
QStringList Control::m_availableStyles;
QNetworkAccessManager *nam = nullptr;

Control::Control(QObject *parent)''',
    '''Control *Control::m_instance = nullptr;
QStringList Control::m_availableStyles;
QNetworkAccessManager *nam = nullptr;

static QVersionNumber releaseVersionNumber(QString version)
{
    if (version.startsWith('v'))
        version.remove(0, 1);
    version.replace("-branchfix.", ".");
    return QVersionNumber::fromString(version);
}

Control::Control(QObject *parent)''',
    "release version parser",
)

replace_once(
    "src/control.cpp",
    '''void Control::checkForUpdates()
{
#ifdef GAM_SELF_UPDATE
    QNetworkRequest req(QUrl(QString("https://gitlab.com/woblight/GitAddonsManager/-/jobs/artifacts/%1/download?job=%2").arg(GAM_BRANCH_NAME).arg(GAM_BUILD_NAME)));
    req.setAttribute(QNetworkRequest::RedirectPolicyAttribute, QNetworkRequest::NoLessSafeRedirectPolicy);
    connect(nam, &QNetworkAccessManager::finished, [](auto reply){
        QApplication::setApplicationDisplayName(reply->errorString());
    });
    auto reply = nam->head(req);
    setUpdateStatus(UpdateStatus::CheckingForUpdate);
    connect(reply, &QNetworkReply::finished,[this, reply](){
        QRegularExpression shaCapt(QString("GitAddonsManager_%1-(\\\\w{40})\\\\.zip").arg(GAM_BUILD_NAME));
        auto match = shaCapt.match(reply->url().toString());
        if (match.hasMatch()) {
            if (!QString(GIT_DESCRIBE).endsWith(match.captured(1).chopped(33)))
                setUpdateStatus(UpdateStatus::UpdateAvailable);
            else setUpdateStatus(UpdateStatus::NoUpdate);
        };
    });
#endif
}''',
    '''void Control::checkForUpdates()
{
#ifdef GAM_SELF_UPDATE
    QNetworkRequest req(QUrl("https://api.github.com/repos/Seraphic8x2244/GitAddonsManager/releases?per_page=1"));
    req.setRawHeader("Accept", "application/vnd.github+json");
    req.setRawHeader("User-Agent", "GitAddonsManager");
    req.setAttribute(QNetworkRequest::RedirectPolicyAttribute, QNetworkRequest::NoLessSafeRedirectPolicy);

    m_updateDownloadUrl.clear();
    auto reply = nam->get(req);
    setUpdateStatus(UpdateStatus::CheckingForUpdate);
    connect(reply, &QNetworkReply::finished,[this, reply](){
        if (reply->error() != QNetworkReply::NoError) {
            setUpdateStatus(UpdateStatus::UpdateError);
            reply->deleteLater();
            return;
        }

        QJsonParseError parseError;
        const auto doc = QJsonDocument::fromJson(reply->readAll(), &parseError);
        if (parseError.error != QJsonParseError::NoError || !doc.isArray() || doc.array().isEmpty()) {
            setUpdateStatus(UpdateStatus::UpdateError);
            reply->deleteLater();
            return;
        }

        const auto release = doc.array().first().toObject();
        const QString latestTag = release.value("tag_name").toString();
        const QVersionNumber latestVersion = releaseVersionNumber(latestTag);
        const QVersionNumber currentVersion = releaseVersionNumber(QStringLiteral(GAM_RELEASE_VERSION));

        if (!latestVersion.isNull() && !currentVersion.isNull() && latestVersion <= currentVersion) {
            setUpdateStatus(UpdateStatus::NoUpdate);
            reply->deleteLater();
            return;
        }
        if (latestVersion.isNull() && latestTag == QStringLiteral(GAM_RELEASE_VERSION)) {
            setUpdateStatus(UpdateStatus::NoUpdate);
            reply->deleteLater();
            return;
        }

        const auto assets = release.value("assets").toArray();
        const QStringList preferredAssetNames = {
            QStringLiteral("GitAddonsManager-Win64.zip"),
            QStringLiteral("GitAddonsManager-Win64-branchfix.zip")
        };
        for (const auto &preferredName : preferredAssetNames) {
            for (const auto &assetValue : assets) {
                const auto asset = assetValue.toObject();
                if (asset.value("name").toString() == preferredName) {
                    m_updateDownloadUrl = QUrl(asset.value("browser_download_url").toString());
                    break;
                }
            }
            if (m_updateDownloadUrl.isValid() && !m_updateDownloadUrl.isEmpty())
                break;
        }

        setUpdateStatus(m_updateDownloadUrl.isValid() && !m_updateDownloadUrl.isEmpty()
                            ? UpdateStatus::UpdateAvailable
                            : UpdateStatus::UpdateError);
        reply->deleteLater();
    });
#endif
}''',
    "GitHub release update check",
)

replace_once(
    "src/control.cpp",
    '''void Control::downloadUpdate()
{
#ifdef GAM_SELF_UPDATE
    QFile *zip = new QFile(QApplication::applicationDirPath() + "/GitAddonsManager.zip");
    if (!zip->open(QFile::WriteOnly)) {
        setUpdateStatus(UpdateStatus::UpdateError);
        return;
    }

    QNetworkRequest req(QUrl(QString("https://gitlab.com/woblight/GitAddonsManager/-/jobs/artifacts/%1/download?job=%2").arg(GAM_BRANCH_NAME).arg(GAM_BUILD_NAME)));
    req.setAttribute(QNetworkRequest::RedirectPolicyAttribute, QNetworkRequest::NoLessSafeRedirectPolicy);
    auto reply = nam->get(req);
    setUpdateStatus(UpdateStatus::DownloadingUpdate);
    connect(reply, &QNetworkReply::readyRead,[reply, zip]() {
        zip->write(reply->readAll());
    });
    connect(reply, &QNetworkReply::finished, [this, reply, zip]() {
        zip->close();
        delete zip;
        setUpdateStatus(reply->error() == QNetworkReply::NoError ? UpdateStatus::UpdateReady : UpdateStatus::UpdateError);
        reply->deleteLater();
    });
    connect(reply, &QNetworkReply::downloadProgress, [this](qint64 recieved, qint64 bytesTotal) {
        setTotal(bytesTotal);
        setProgress(recieved);
    });
#endif
}''',
    '''void Control::downloadUpdate()
{
#ifdef GAM_SELF_UPDATE
    if (!m_updateDownloadUrl.isValid() || m_updateDownloadUrl.isEmpty()) {
        setUpdateStatus(UpdateStatus::UpdateError);
        return;
    }

    QFile *zip = new QFile(QApplication::applicationDirPath() + "/GitAddonsManager.zip");
    if (!zip->open(QFile::WriteOnly)) {
        delete zip;
        setUpdateStatus(UpdateStatus::UpdateError);
        return;
    }

    QNetworkRequest req(m_updateDownloadUrl);
    req.setRawHeader("User-Agent", "GitAddonsManager");
    req.setAttribute(QNetworkRequest::RedirectPolicyAttribute, QNetworkRequest::NoLessSafeRedirectPolicy);
    auto reply = nam->get(req);
    setUpdateStatus(UpdateStatus::DownloadingUpdate);
    connect(reply, &QNetworkReply::readyRead,[reply, zip]() {
        zip->write(reply->readAll());
    });
    connect(reply, &QNetworkReply::finished, [this, reply, zip]() {
        zip->write(reply->readAll());
        zip->close();
        delete zip;
        setUpdateStatus(reply->error() == QNetworkReply::NoError ? UpdateStatus::UpdateReady : UpdateStatus::UpdateError);
        reply->deleteLater();
    });
    connect(reply, &QNetworkReply::downloadProgress, [this](qint64 received, qint64 bytesTotal) {
        setTotal(bytesTotal);
        setProgress(received);
    });
#endif
}''',
    "GitHub release update download",
)

replace_once(
    "src/control.cpp",
    '''        QuaZip zip(appRoot.absoluteFilePath("GitAddonsManager.zip"));
        if (!zip.open(QuaZip::mdUnzip))
            return;
        QDir root(appRoot.absoluteFilePath("update"));
        appRoot.mkdir(root.absolutePath());
        unsigned int size = 0;
        foreach (const QuaZipFileInfo &info, zip.getFileInfoList())
            size += info.uncompressedSize;
        setTotal(size);
        size = 0;
        foreach (const QuaZipFileInfo &info, zip.getFileInfoList()) {
            QuaZipFile z(zip.getZipName(), info.name);
            z.open(QuaZipFile::ReadOnly);
            QFileInfo finfo(root.absoluteFilePath(info.name.section("/",1)));
            root.mkpath(finfo.absolutePath());
            QFile f(finfo.absoluteFilePath());
            f.open(QFile::WriteOnly);
            QByteArray chunk;
            while (!(chunk = z.read(32*1024)).isEmpty()) {
                f.write(chunk);
                size += chunk.size();
                setProgress(size);
            }
            f.close();
        }''',
    '''        QuaZip zip(appRoot.absoluteFilePath("GitAddonsManager.zip"));
        if (!zip.open(QuaZip::mdUnzip)) {
            setUpdateStatus(UpdateStatus::UpdateError);
            return;
        }
        QDir root(appRoot.absoluteFilePath("update"));
        appRoot.mkpath(root.absolutePath());
        unsigned int size = 0;
        foreach (const QuaZipFileInfo &info, zip.getFileInfoList())
            size += info.uncompressedSize;
        setTotal(size);
        size = 0;
        foreach (const QuaZipFileInfo &info, zip.getFileInfoList()) {
            QString relativePath = QDir::cleanPath(info.name);
            if (relativePath.isEmpty() || relativePath == "." || relativePath == ".." ||
                relativePath.startsWith("../") || QDir::isAbsolutePath(relativePath))
                continue;
            if (info.name.endsWith('/')) {
                root.mkpath(relativePath);
                continue;
            }

            QuaZipFile z(zip.getZipName(), info.name);
            if (!z.open(QuaZipFile::ReadOnly))
                continue;
            QFileInfo finfo(root.absoluteFilePath(relativePath));
            root.mkpath(finfo.absolutePath());
            QFile f(finfo.absoluteFilePath());
            if (!f.open(QFile::WriteOnly))
                continue;
            QByteArray chunk;
            while (!(chunk = z.read(32*1024)).isEmpty()) {
                f.write(chunk);
                size += chunk.size();
                setProgress(size);
            }
            f.close();
        }''',
    "root-level update ZIP extraction",
)

replace_once(
    "src/control.h",
    '''    UpdateStatus m_updateStatus = UpdateStatus::NoUpdate;

    QStringList m_addonsPaths;''',
    '''    UpdateStatus m_updateStatus = UpdateStatus::NoUpdate;

    QUrl m_updateDownloadUrl;

    QStringList m_addonsPaths;''',
    "update download URL state",
)

replace_once(
    "src/control.h",
    '''    QString m_version = QString("%1 (%2 %3)").arg(GIT_DESCRIBE)
#ifdef GAM_BUILD_NAME
                                                                   .arg(GAM_BUILD_NAME)
#else
                                                                   .arg(QSysInfo::productType())
#endif
#ifdef GAM_BANCH_NAME
                                                                   .arg(GAM_BANCH_NAME)
#else
                                                                   .arg(QSysInfo::buildCpuArchitecture())
#endif
                                                 ;''',
    '''    QString m_version = QString("%1 / upstream %2 (%3 %4)").arg(GAM_RELEASE_VERSION).arg(GIT_DESCRIBE)
#ifdef GAM_BUILD_NAME
                                                                   .arg(GAM_BUILD_NAME)
#else
                                                                   .arg(QSysInfo::productType())
#endif
#ifdef GAM_BRANCH_NAME
                                                                   .arg(GAM_BRANCH_NAME)
#else
                                                                   .arg(QSysInfo::buildCpuArchitecture())
#endif
                                                 ;''',
    "display release version",
)

replace_once(
    "src/main.qml",
    '''                Label {
                    text: "Author: woblight <woblight@gmail.com>"
                }
                Label {
                    text: "Source code: <a href=\\"https://gitlab.com/woblight/GitAddonsManager\\">GitLab</a>"
                    onLinkActivated: Qt.openUrlExternally(link)
                    textFormat: Text.RichText
                }
                Label {
                    text: "Report an issue: <a href=\\"https://gitlab.com/woblight/GitAddonsManager/-/issues\\">GitLab</a>"
                    onLinkActivated: Qt.openUrlExternally(link)
                    textFormat: Text.RichText
                }''',
    '''                Label {
                    text: "Original author: woblight <woblight@gmail.com>"
                }
                Label {
                    text: "Source code: <a href=\\"https://github.com/Seraphic8x2244/GitAddonsManager\\">GitHub</a>"
                    onLinkActivated: Qt.openUrlExternally(link)
                    textFormat: Text.RichText
                }
                Label {
                    text: "Report an issue: <a href=\\"https://github.com/Seraphic8x2244/GitAddonsManager/issues\\">GitHub</a>"
                    onLinkActivated: Qt.openUrlExternally(link)
                    textFormat: Text.RichText
                }
                Label {
                    text: "Upstream source: <a href=\\"https://gitlab.com/woblight/GitAddonsManager\\">GitLab</a>"
                    onLinkActivated: Qt.openUrlExternally(link)
                    textFormat: Text.RichText
                }''',
    "About page repository links",
)

print("Applied GitAddonsManager maintained-fork enhancements.")
