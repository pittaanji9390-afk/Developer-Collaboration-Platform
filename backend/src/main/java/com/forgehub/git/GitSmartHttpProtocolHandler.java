package com.forgehub.git;

import com.forgehub.authorization.RepoAccessService;
import com.forgehub.identity.UserPrincipal;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.shared.exception.ApiException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.jgit.http.server.GitSmartHttpTools;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.transport.PacketLineOut;
import org.eclipse.jgit.transport.ReceivePack;
import org.eclipse.jgit.transport.UploadPack;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;

@Slf4j
@RestController
@RequestMapping("/api/v1/git-http/{owner}/{slug}.git")
@RequiredArgsConstructor
public class GitSmartHttpProtocolHandler {

    private final JGitService jgitService;
    private final RepositoryRepository repoRepository;
    private final RepoAccessService repoAccessService;

    @GetMapping("/info/refs")
    public void getInfoRefs(
            @PathVariable String owner,
            @PathVariable String slug,
            @RequestParam String service,
            @AuthenticationPrincipal UserPrincipal principal,
            HttpServletRequest request,
            HttpServletResponse response
    ) throws IOException {

        RepositoryEntity repoEntity = getAndVerifyRepo(owner, slug, service, principal);
        Repository repo = jgitService.openRepository(repoEntity.getRepositoryPath());

        response.setContentType("application/x-" + service + "-advertisement");
        response.setHeader("Expires", "Fri, 01 Jan 1980 00:00:00 GMT");
        response.setHeader("Pragma", "no-cache");
        response.setHeader("Cache-Control", "no-cache, max-age=0, must-revalidate");

        OutputStream out = response.getOutputStream();
        PacketLineOut packetOut = new PacketLineOut(out);
        packetOut.writeString("# service=" + service + "\n");
        packetOut.end();

        if ("git-upload-pack".equals(service)) {
            UploadPack uploadPack = new UploadPack(repo);
            uploadPack.sendAdvertisedRefs(new org.eclipse.jgit.transport.RefAdvertiser.PacketLineOutRefAdvertiser(packetOut));
        } else if ("git-receive-pack".equals(service)) {
            ReceivePack receivePack = new ReceivePack(repo);
            receivePack.sendAdvertisedRefs(new org.eclipse.jgit.transport.RefAdvertiser.PacketLineOutRefAdvertiser(packetOut));
        } else {
            response.sendError(HttpServletResponse.SC_FORBIDDEN, "Unsupported service: " + service);
        }
    }

    @PostMapping("/git-upload-pack")
    public void uploadPack(
            @PathVariable String owner,
            @PathVariable String slug,
            @AuthenticationPrincipal UserPrincipal principal,
            HttpServletRequest request,
            HttpServletResponse response
    ) throws IOException {

        RepositoryEntity repoEntity = getAndVerifyRepo(owner, slug, "git-upload-pack", principal);
        Repository repo = jgitService.openRepository(repoEntity.getRepositoryPath());

        response.setContentType("application/x-git-upload-pack-result");
        response.setHeader("Cache-Control", "no-cache");

        InputStream in = request.getInputStream();
        if ("gzip".equalsIgnoreCase(request.getHeader("Content-Encoding"))) {
            in = new GZIPInputStream(in);
        }

        OutputStream out = response.getOutputStream();
        UploadPack uploadPack = new UploadPack(repo);
        uploadPack.upload(in, out, null);
    }

    @PostMapping("/git-receive-pack")
    public void receivePack(
            @PathVariable String owner,
            @PathVariable String slug,
            @AuthenticationPrincipal UserPrincipal principal,
            HttpServletRequest request,
            HttpServletResponse response
    ) throws IOException {

        RepositoryEntity repoEntity = getAndVerifyRepo(owner, slug, "git-receive-pack", principal);
        Repository repo = jgitService.openRepository(repoEntity.getRepositoryPath());

        response.setContentType("application/x-git-receive-pack-result");
        response.setHeader("Cache-Control", "no-cache");

        InputStream in = request.getInputStream();
        if ("gzip".equalsIgnoreCase(request.getHeader("Content-Encoding"))) {
            in = new GZIPInputStream(in);
        }

        OutputStream out = response.getOutputStream();
        ReceivePack receivePack = new ReceivePack(repo);
        receivePack.receive(in, out, null);
    }

    private RepositoryEntity getAndVerifyRepo(String owner, String slug, String service, UserPrincipal principal) {
        RepositoryEntity repo = repoRepository.findByOwnerUserUsernameAndSlug(owner, slug)
                .or(() -> repoRepository.findByOrganizationSlugAndSlug(owner, slug))
                .orElseThrow(() -> ApiException.notFound("Repository not found: " + owner + "/" + slug));

        if ("git-upload-pack".equals(service)) {
            if (!repoAccessService.canRead(principal, repo.getId())) {
                throw ApiException.unauthorized("Authentication required to read repository");
            }
        } else if ("git-receive-pack".equals(service)) {
            if (!repoAccessService.canWrite(principal, repo.getId())) {
                throw ApiException.forbidden("Write permissions required to push to repository");
            }
        }
        return repo;
    }
}
